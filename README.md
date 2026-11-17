# Deploy Board

Small Full-Stack application with an emphasis on CI/CD pipelines

## Startup
**Backend**
Linux/macOS
```bash
cd ./backend

uv sync

<<<<<<< HEAD
source ./.venv/bin/activate # If not already in .venv

uvicorn main:app --reload
```  

Windows
```powershell
cd .\backend

uv sync

source .\.venv\Scripts\activate # If not already in .venv

uvicorn main:app --reload
```  
=======
uvicorn main:app ---reload
```
>>>>>>> main
