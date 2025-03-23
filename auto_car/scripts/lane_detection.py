import cv2
import numpy as np

class LaneDetector:
    def __init__(self, kernel_size=5, low_t=50, high_t=150):
        self.kernel_size = kernel_size
        self.low_t = low_t
        self.high_t = high_t

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
            [(int(0.1 * width), height),        # Bottom-left corner
             (int(0.4 * width), int(0.6 * height)),  # Lower center-left
             (int(0.6 * width), int(0.6 * height)),  # Lower center-right
             (int(0.9 * width), height)]        # Bottom-right corner
        ], np.int32)
        cv2.fillPoly(mask, polygon, 255)
        return cv2.bitwise_and(image, mask)

    def hough_transform(self, image):
        return cv2.HoughLinesP(image, 1, np.pi / 180, 20, minLineLength=20, maxLineGap=500)

    def average_slope_intercept(self, lines):
        left_lines, right_lines = [], []
        for line in lines:
            x1, y1, x2, y2 = line[0]
            slope = (y2 - y1) / (x2 - x1) if x2 - x1 != 0 else 0
            if slope < 0:
                left_lines.append(line)
            else:
                right_lines.append(line)
        return left_lines, right_lines

    def draw_lane_lines(self, image, lines):
        line_image = np.zeros_like(image)
        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                cv2.line(line_image, (x1, y1), (x2, y2), (0, 255, 0), 5)
        return cv2.addWeighted(image, 0.8, line_image, 1, 1)

    def process_frame(self, frame):
        gray = self.grayscale(frame)
        blur = self.gaussian_blur(gray)
        edges = self.canny_edge_detection(blur)
        region = self.region_selection(edges)
        lines = self.hough_transform(region)
        if lines is not None:
            left_lines, right_lines = self.average_slope_intercept(lines)
            frame = self.draw_lane_lines(frame, left_lines + right_lines)
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
