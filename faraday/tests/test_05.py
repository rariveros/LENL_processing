from directories import *
from back_process import *


if __name__ == "__main__":

    ### Definiendo parametros y eligiendo carpeta a detectar ###
    resize_scale = 1
    thresh = 48

    def nan_helper(y):
        return np.isnan(y), lambda z: z.nonzero()[0]
    ### Abriendo imagen de referencia para determinar la región de interes (ROI) y la conversion a mm ###
    root = tk.Tk()
    root.withdraw()
    reference_image = "E:/mnustes_science/images/img_lab/PT_01/f=15.20_a=12.0/cam000000.jpg"
    img_reference = cv2.imread(str(reference_image))

    ### Binarize images with 0 and 1 ###
    gamma = 3.5
    alpha = 10
    beta = -20
    img_processed = image_corrections(img_reference, alpha, beta, gamma)
    cv2.imshow("OLA", img_processed)
    cv2.waitKey(0)  # waits until a key is pressed
    cv2.destroyAllWindows()  # destroys the window showing image