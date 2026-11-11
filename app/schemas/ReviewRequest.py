from pydantic import BaseModel, Field, field_validator

# Definizione classe
class ReviewRequest(BaseModel):
    review: str = Field(min_length=1, max_length=5000)

    @field_validator('review', mode='before')
    @classmethod
    def validate_review(cls, value: str) -> str:
        # Evita crash se l'input non è una stringa e in seguito rimuove gli spazi vuoti all'inizio e alla fine
        if not isinstance(value, str):
            return value
        cleaned_value = value.strip()
        
        # Se dopo lo strip la stringa è vuota, solleva un errore
        if not cleaned_value:
            raise ValueError("La recensione non può contenere solo spazi vuoti.")
            
        # Altrimenti restituisce il testo ripulito completo
        return cleaned_value
