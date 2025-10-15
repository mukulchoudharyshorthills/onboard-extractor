flowchart TD
    A[User uploads a document] --> B[/upload API triggered/]
    B --> C[Save data in DB for user & document]
    C --> D{Document Type?}
    
    D -->|PDF| E[Convert PDF to images using PyMuPDF]
    E --> F[Send image data to Gemini/Azure/OpenAI for OCR]

    D -->|Image| F[Send image data to Gemini/Azure/OpenAI for OCR]
    
    F --> G[AI processes and returns JSON]
    G --> H[Save JSON to DB for the document]
    H --> I[Send data to frontend for user verification/edit]

    I --> J{User Action?}
    J -->|Verify| K[/verify API triggered/]
    K --> L[Update DB - Verified by user]

    J -->|Edit| M[/edit API triggered/]
    M --> N[Update DB - Edited & Verified by user]
    