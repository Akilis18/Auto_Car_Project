import cv2
import numpy as np

class LaneDetector:
    def __init__(self, kernel_size=5, low_t=50, high_t=150):
        self.kernel_size = kernel_size
        self.low_t = low_t
        self.high_t = high_t
        self.prev_left = None
        self.prev_right = None

    def grayscale(self, image):
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    def gaussian_blur(self, image):
        return cv2.GaussianBlur(image, (self.kernel_size, self.kernel_size), 0)

    def canny_edge_detection(self, image):
        return cv2.Canny(image, self.low_t, self.high_t)

    def region_selection(self, image):
        height, width = image.shape[:2]
        mask = np.zeros_like(image)
        polygon = np.array([
            [(int(0.1 * width), height),              # Bottom-left
             (int(0.1 * width), int(0.6 * height)),   # Top-left
             (int(0.9 * width), int(0.6 * height)),   # Top-right
             (int(0.9 * width), height)]              # Bottom-right
        ], np.int32)
        cv2.fillPoly(mask, polygon, 255)
        return cv2.bitwise_and(image, mask)

    def hough_transform(self, image):
        return cv2.HoughLinesP(image, 1, np.pi / 180, 20, minLineLength=20, maxLineGap=500)

    def make_line_from_fit(self, line_params, height):
        if len(line_params) < 2:
            return None  # Not enough data to average
        slope, intercept = np.mean(line_params, axis=0)
        y1 = height
        y2 = int(height * 0.6)
        if slope == 0:
            return None
        x1 = int((y1 - intercept) / slope)
        x2 = int((y2 - intercept) / slope)
        return [(x1, y1, x2, y2)]

    def average_slope_intercept(self, lines, height):
        left_fit = []
        right_fit = []

        for line in lines:
            x1, y1, x2, y2 = line[0]
            if x2 - x1 == 0:
                continue  # Skip vertical lines
            slope = (y2 - y1) / (x2 - x1)
            if abs(slope) < 0.3:  # Filter nearly horizontal lines
                continue
            intercept = y1 - slope * x1
            if slope < 0:
                left_fit.append((slope, intercept))
            else:
                right_fit.append((slope, intercept))

        left_line = self.make_line_from_fit(left_fit, height)
        right_line = self.make_line_from_fit(right_fit, height)

        # Reuse previous if current is missing
        if left_line is None and self.prev_left is not None:
            left_line = self.prev_left
        elif left_line is not None:
            self.prev_left = left_line

        if right_line is None and self.prev_right is not None:
            right_line = self.prev_right
        elif right_line is not None:
            self.prev_right = right_line

        return [left_line, right_line]

    def draw_lane_lines(self, image, lines):
        line_image = np.zeros_like(image)
        if lines is not None:
            for line in lines:
                if line is not None:
                    x1, y1, x2, y2 = line[0]
                    cv2.line(line_image, (x1, y1), (x2, y2), (0, 255, 0), 5)
        return cv2.addWeighted(image, 0.8, line_image, 1, 1)

    def process_frame(self, frame):
        height = frame.shape[0]
        gray = self.grayscale(frame)
        blur = self.gaussian_blur(gray)
        edges = self.canny_edge_detection(blur)
        region = self.region_selection(edges)
        lines = self.hough_transform(region)
        if lines is not None:
            fitted_lines = self.average_slope_intercept(lines, height)
            frame = self.draw_lane_lines(frame, fitted_lines)
        return frame

    def process_video(self, input_path, output_path):
        cap = cv2.VideoCapture(input_path)
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(output_path, fourcc, 30.0, (int(cap.get(3)), int(cap.get(4))))

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            processed_frame = self.process_frame(frame)
            out.write(processed_frame)

        cap.release()
        out.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    detector = LaneDetector()
    detector.process_video('input.mp4', 'output.mp4')
