import numpy as np

class GLCM:

    def __init__(self, data):

        self.data = np.array(data).astype(np.float32)

    ##速度マトリクスをscaledマトリクスに変換する関数
    @staticmethod
    def _convert_scaled_matrix(x):

        if x > 150:
            return int(16)
        elif x == 0:
            return int(0)
        else:
            return int(- (- x // 10))

    ##scaledマトリクスをGLCMに変換する関数
    @staticmethod
    def _convert_glcm(scaled_matrix):

        glcm_matrix = np.zeros((16, 16))

        for row in scaled_matrix:
            for i in range(len(row) - 1):

                if row[i] and row[i + 1]:

                    glcm_row = int(row[i] - 1)
                    glcm_col = int(row[i + 1] - 1)
                    glcm_matrix[glcm_row, glcm_col] += 1

        return glcm_matrix

    ##glcmを返す関数
    def glcm(self, lange, time_index):

        scaled_matrix = np.vectorize(self._convert_scaled_matrix)(self.data)
        range_matrix = scaled_matrix[:, time_index - lange + 1:time_index + 1]
        glcm_matrix = self._convert_glcm(range_matrix)

        return glcm_matrix
