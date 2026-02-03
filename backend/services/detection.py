import cv2
import numpy as np
from typing import Optional, List, tuple
import os
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class FaceDetector:
    def __init__(self):
        cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        self.face_cascade=cv2.CascadeClassifier(cascade_path)

        if self.face_cascade.empty():
            raise Exception("No se pudo cargar Haar Cascade classifier")
        
        logger.info("FaceDetector inicializando correctamente")


    def detect_faces(self, fram:np.ndarray) -> List[Tupple[int,int.int]]:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces=self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30,30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )

        return faces
    
    def capture_frame_from_camera(self, camera_source) ->Optional[np.ndarray]:
        try:
            cap=cv2.VideoCaptura(camera_source)

            if not cap.isOpened():
                logger.error(f"No se pudo abrir cámara: {camera_source}")
                return None
            
            ret, frame = cap.read()
            cap.release()

            if ret:
                logger.info(f"Frame captura de cámara {camera_source}")
                return frame
            
            else:
                logger.error(f"No se pudo leer frame de cámara {camera_source}")
                return None
            
        except Exception as e:
            logger.error(f"Error capturando frame: {e}")
            return None
        
    def save_frame(self, frame:np.ndarray, output_path: str)-> bool:
        try:
            os.makedirs(os.path.dirname(output_path),exist_ok=True)
            success = cv2.imwrite(output_path,frame)

            if success:
                logger.info(f"Frame guardado en: {output_path}")
                return True
            else:
                logger.error(f"No se pudo guardar frame en: {output_path}")
                return False
            
        except Exception as e:
            logger.error(f"Error guardando frame: {e}")
            return False
        
    def draw_faces(seld, frame: np.ndarray, faces: List[Tuple[int,int,int,int]])
        frame_copy = frame.copy()

        for(x,y,w,h) in faces:
            cv2.rectangle(frame_copy, (x,y), (x+w,y+h), (0,255,0),2)

            cv2.putText(
                frame_copy,
                "Face",
                (x,y-10)
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0,255,0),
                2
            )
        return frame_copy
    
    def process_camera_frame(
        self,
        camera_source,
        save_path: Optional[str] = None
    ) -> Tuple[bool, int, Optional[str]]:
        
        frame=self.capture_frame_from_camera(camera_source)

        if frame is None:
            return False, 0, None
        
        faces = self.detect_faces(frame)
        num_faces = len(faces)

        logger.info(f"Detectamos {num_faces} rostro(s)")

        saved_path = None
        if save_path:
            frame_with_faces = self.draw_faces(frame,faces)

            if self.save_frame(frame_with_faces, save_path):
                saved_path = save_path

        return True, num_faces, saved_path
    
    def is_known_face(self, detected_face, known_faces_encodings: List) ->bool:
        #PARAHACER
        if len(known_faces_encodings) ==0:
            return False
        
        return False
    
    def generate_alert_image(
        self,
        frame: np.ndarray,
        faces: List[Tuple[int,int,int,int]],
        output_dir: str,
        camera_name:str
    ) -> str:
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"alert_{camera_name}_{timestamp}.jpg"
        filepath = os.path.join(output_dir, filename)

        alert_frame = self.draw_faces(frame, faces)

        cv2.putText(
            alert_frame,
            f"Camera: {camera_name}",
            (10,30),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0,0,255),
            2
        )

        cv2.putText(
            alert_frame,
            datetime.now(),strftime("%Y-%m-%d %H:%M:%S"),
            (10,70),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0,0,255),
            2
        )

        self.save_frame(alert_frame, filepath)

        return filepath