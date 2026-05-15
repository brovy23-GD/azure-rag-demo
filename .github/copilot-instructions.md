# GitHub Copilot Instructions

## Who I Am
Bobby Rovy | MSSA CAD (Cloud Application Development) Program
Focus: C# / .NET, Data Structures, Algorithms, Cloud Infrastructure (Azure)

## Primary Tech Stack
- Language: C# (.NET 8 / .NET Core), Python, HCL (Terraform)
- - Frameworks: FastAPI (Python), LangChain (AI/RAG pipelines)
  - - Cloud: Azure (Bicep IaC, Azure AI, Azure Container Apps)
    - - Tools: Docker, Terraform, Git
     
      - ## Coding Standards (C#)
      - - Always use strong typing - no implicit var unless type is obvious
        - - Follow PascalCase for classes/methods, camelCase for local variables
          - - Add XML doc comments on all public methods and classes
            - - Use async/await for I/O operations - never block with .Result or .Wait()
              - - Apply SOLID principles and clean architecture patterns
                - - Prefer LINQ over manual loops for collections where readable
                 
                  - ## Algorithm & Data Structure Rules
                  - - Always include Big O time and space complexity in comments
                    - - Explain the approach in plain English above the solution
                      - - Prefer optimal solutions but show reasoning step by step
                        - - Write self-documenting code - variable names should explain intent
                         
                          - ## Testing
                          - - Unit tests for every non-trivial method
                            - - Use descriptive names: Should_[ExpectedResult]_When_[Condition]
                              - - Mock external dependencies - never hit real APIs or databases in tests
                               
                                - ## Error Handling
                                - - Never swallow exceptions silently
                                  - - Always log with meaningful context messages
                                    - - Use Result>T> patterns or custom exceptions over generic Exception
                                     
                                      - ## Python Standards
                                      - - Follow PEP 8 strictly
                                        - - Use type hints on all function signatures
                                          - - Prefer pathlib over os.path
                                            - - Use dataclasses or Pydantic models for structured data
                                             
                                              - ## Infrastructure (HCL / Bicep)
                                              - - Always include descriptions on all variables and outputs
                                                - - Tag all Azure resources with environment, owner, and project
                                                  - - Use modules for reusable infrastructure components
                                                    - - Never hardcode secrets - use Key Vault references or env vars
                                                     
                                                      - ## What to Avoid
                                                      - - No magic numbers - use named constants
                                                        - - No commented-out dead code
                                                          - - No Console.WriteLine in production - use ILogger
                                                            - - No hardcoded connection strings or API keys
