import uuid
import json
from app.database import db
from app.agent import Agent



class Consultation:
    def __init__(self,record_id=None, patient_id=None, doctor_id=None, organization_id=None, transcript=None):
        self.record_id = record_id if record_id else uuid.uuid4().hex
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.organization_id = organization_id
        self.transcript = transcript
        self.top_5_disease = None
        self.prescribed_medicine = None
        self.transcript_summary = None
        self._db = db

    def create(self):
        """
        Creates a new consultation record.
        Returns:
            record_id: If the consultation record is successfully created.
        """
        record_id = self._db.create_consultation_record(self.record_id, self.patient_id, self.doctor_id, self.organization_id)
        return record_id
    
    def get_previous_consultation_records(self):
        """
        Retrieves the previous consultation record for the patient.
        Returns:
            record: The consultation record if found, None otherwise.
        """
        record = self._db.get_consultation_records(self.patient_id)
        return record
    
    def update(self):
        """
        Updates the consultation record with the transcript.
        Returns:
            bool: True if the record is successfully updated, False otherwise.
        """
        try:
            self._db.update_consultation_record(self.record_id, self.transcript_summary, self.top_5_disease, self.prescribed_medicine)
            return True
        except Exception as e:
            raise RuntimeError(f"Error updating consultation record: {e}")
    
    def analyze_transcript(self):
        """
        Analyzes the transcript to extract top 5 diseases, prescribed medicine, and summary.
        Returns:
            tuple: A tuple containing:
                - top_5_disease: List of top 5 diseases.
                - prescribed_medicine: List of prescribed medicines.
                - transcript_summary: Summary of the consultation.
        """
        try:
            agent = Agent()
            response = agent.analyze_transcript(transcript=self.transcript)
            response = json.loads(response)
            self.top_5_disease = response['top_5_disease']
            self.prescribed_medicine = response['prescribed_medicine']
            self.transcript_summary = response['transcript_summary']
            return response
        except Exception as e:
            raise RuntimeError(f"Error analyzing transcript: {e}")
        
        finally:
            self.update()