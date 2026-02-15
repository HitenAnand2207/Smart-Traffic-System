import numpy as np
import cv2
from typing import Dict, Tuple
import supervision as sv

class HeatmapGenerator:
    """
    Generate traffic density heatmaps and congestion visualizations.
    """
    
    def __init__(self, frame_width: int = 1280, frame_height: int = 720, grid_size: int = 32):
        """
        Initialize heatmap generator.
        
        Args:
            frame_width: Video frame width
            frame_height: Video frame height
            grid_size: Size of grid cells for heatmap
        """
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.grid_size = grid_size
        self.grid_cols = (frame_width + grid_size - 1) // grid_size
        self.grid_rows = (frame_height + grid_size - 1) // grid_size
        
        # Initialize grid accumulator
        self.vehicle_density = np.zeros((self.grid_rows, self.grid_cols), dtype=np.float32)
        self.visit_counts = np.zeros((self.grid_rows, self.grid_cols), dtype=np.int32)
        self.temporal_accumulator = np.zeros((self.grid_rows, self.grid_cols), dtype=np.float32)
        
    def update(self, detections: sv.Detections):
        """
        Update heatmap with current detections.
        """
        # Decay temporal history
        self.temporal_accumulator *= 0.95
        
        # Add current vehicle positions
        for box in detections.xyxy:
            center_x = (box[0] + box[2]) / 2
            center_y = (box[1] + box[3]) / 2
            
            grid_x = int(center_x // self.grid_size)
            grid_y = int(center_y // self.grid_size)
            
            # Ensure within bounds
            grid_x = max(0, min(grid_x, self.grid_cols - 1))
            grid_y = max(0, min(grid_y, self.grid_rows - 1))
            
            self.vehicle_density[grid_y, grid_x] += 1
            self.visit_counts[grid_y, grid_x] += 1
            self.temporal_accumulator[grid_y, grid_x] += 1
    
    def get_density_heatmap(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Get current density heatmap.
        
        Returns:
            heatmap: Normalized heatmap (0-1)
            grid: Grid data for visualization
        """
        # Normalize
        max_density = np.max(self.vehicle_density) if np.max(self.vehicle_density) > 0 else 1
        normalized = self.vehicle_density / max_density
        
        # Smooth with Gaussian blur
        grid = cv2.GaussianBlur((normalized * 255).astype(np.uint8), (5, 5), 0)
        grid = grid.astype(np.float32) / 255.0
        
        return normalized, grid
    
    def get_temporal_heatmap(self) -> np.ndarray:
        """
        Get temporal (accumulated) heatmap showing high-traffic zones over time.
        """
        max_temp = np.max(self.temporal_accumulator) if np.max(self.temporal_accumulator) > 0 else 1
        normalized = self.temporal_accumulator / max_temp
        
        grid = cv2.GaussianBlur((normalized * 255).astype(np.uint8), (7, 7), 0)
        return grid.astype(np.float32) / 255.0
    
    def render_heatmap_on_frame(self, frame: np.ndarray, use_temporal: bool = False) -> np.ndarray:
        """
        Overlay heatmap on frame.
        
        Args:
            frame: Input frame
            use_temporal: Use temporal accumulation instead of current density
            
        Returns:
            Frame with heatmap overlay
        """
        if use_temporal:
            heatmap = self.get_temporal_heatmap()
        else:
            _, heatmap = self.get_density_heatmap()
        
        # Resize heatmap to frame size
        heatmap_resized = cv2.resize(
            heatmap,
            (frame.shape[1], frame.shape[0]),
            interpolation=cv2.INTER_LINEAR
        )
        
        # Apply colormap
        heatmap_colored = cv2.applyColorMap((heatmap_resized * 255).astype(np.uint8), cv2.COLORMAP_JET)
        
        # Blend with original frame
        overlay = cv2.addWeighted(frame, 0.6, heatmap_colored, 0.4, 0)
        
        return overlay
    
    def get_hotspots(self, threshold: float = 0.5) -> list:
        """
        Identify traffic hotspots (high-density areas).
        
        Args:
            threshold: Density threshold for hotspot detection
            
        Returns:
            List of hotspot regions
        """
        _, heatmap = self.get_density_heatmap()
        
        # Find cells above threshold
        hotspots = []
        for y in range(heatmap.shape[0]):
            for x in range(heatmap.shape[1]):
                if heatmap[y, x] > threshold:
                    pixel_x = x * self.grid_size
                    pixel_y = y * self.grid_size
                    hotspots.append({
                        'grid_x': x,
                        'grid_y': y,
                        'pixel_x': pixel_x,
                        'pixel_y': pixel_y,
                        'density': float(heatmap[y, x]),
                        'box': (pixel_x, pixel_y, pixel_x + self.grid_size, pixel_y + self.grid_size)
                    })
        
        return sorted(hotspots, key=lambda h: h['density'], reverse=True)
    
    def get_congestion_index_by_region(self) -> Dict[str, float]:
        """
        Calculate congestion index for different regions of the frame.
        """
        h, w = self.vehicle_density.shape
        
        # Divide into 9 regions (3x3 grid)
        region_h = h // 3
        region_w = w // 3
        
        regions = {
            'top_left': self.vehicle_density[0:region_h, 0:region_w].mean(),
            'top_center': self.vehicle_density[0:region_h, region_w:2*region_w].mean(),
            'top_right': self.vehicle_density[0:region_h, 2*region_w:].mean(),
            'mid_left': self.vehicle_density[region_h:2*region_h, 0:region_w].mean(),
            'mid_center': self.vehicle_density[region_h:2*region_h, region_w:2*region_w].mean(),
            'mid_right': self.vehicle_density[region_h:2*region_h, 2*region_w:].mean(),
            'bottom_left': self.vehicle_density[2*region_h:, 0:region_w].mean(),
            'bottom_center': self.vehicle_density[2*region_h:, region_w:2*region_w].mean(),
            'bottom_right': self.vehicle_density[2*region_h:, 2*region_w:].mean(),
        }
        
        return regions
    
    def reset(self):
        """
        Reset heatmap data.
        """
        self.vehicle_density = np.zeros((self.grid_rows, self.grid_cols), dtype=np.float32)
        self.visit_counts = np.zeros((self.grid_rows, self.grid_cols), dtype=np.int32)
        self.temporal_accumulator = np.zeros((self.grid_rows, self.grid_cols), dtype=np.float32)
    
    def draw_grid_overlay(self, frame: np.ndarray, show_numbers: bool = False) -> np.ndarray:
        """
        Draw grid overlay on frame for reference.
        """
        annotated = frame.copy()
        
        # Draw vertical lines
        for x in range(0, frame.shape[1], self.grid_size):
            cv2.line(annotated, (x, 0), (x, frame.shape[0]), (200, 200, 200), 1)
        
        # Draw horizontal lines
        for y in range(0, frame.shape[0], self.grid_size):
            cv2.line(annotated, (0, y), (frame.shape[1], y), (200, 200, 200), 1)
        
        # Optional: draw congestion level numbers
        if show_numbers:
            _, heatmap = self.get_density_heatmap()
            for y in range(heatmap.shape[0]):
                for x in range(heatmap.shape[1]):
                    if heatmap[y, x] > 0.1:
                        px = x * self.grid_size + self.grid_size // 2
                        py = y * self.grid_size + self.grid_size // 2
                        cv2.putText(
                            annotated,
                            f"{heatmap[y, x]:.1f}",
                            (px - 10, py + 5),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.4,
                            (255, 255, 255),
                            1
                        )
        
        return annotated
