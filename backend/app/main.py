from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
from ocr import run_ocr
from extractor import extract_transactions
from scoring import compute_credit_trust_score
from pdf_report import generate_pdf_report
from ai_analyzer import analyze_with_ai
import io

app = FastAPI(title="Smart Credit Analysis API (OpenAI-enabled)")

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/analyze")
async def analyze(file: UploadFile = File(...), include_nl_summary: bool = True):
    if file.content_type not in ["application/pdf", "image/png", "image/jpeg"]:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    content = await file.read()
    ocr_result = run_ocr(content, content_type=file.content_type)
    transactions = extract_transactions(ocr_result)
    score, explanation = compute_credit_trust_score(transactions)

    # Use OpenAI to enrich analysis (stateless call)
    ai_summary = analyze_with_ai(transactions, score, explanation, use_openai=True) if include_nl_summary else None

    pdf_bytes = generate_pdf_report(score, explanation, transactions, ai_summary)

    return StreamingResponse(io.BytesIO(pdf_bytes), media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=credit_report_{file.filename}.pdf"})
