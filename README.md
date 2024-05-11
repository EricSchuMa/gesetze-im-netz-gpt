## Getting Started

### Prerequisites

- Docker
- Python 3.10
- Poetry for Python dependency management

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/EricSchuMa/gesetze-im-netz-gpt
   cd gesetze-im-netz-gpt
   ```

2. **Build the Docker container:**

    Navigate to the root directory where the Dockerfile is located and run:
    ```bash
    docker build -t gesetze-im-netz-gpt .
    ```

3. **Run the Docker container:**

    ```bash
   docker run -p 8000:8000 gesetze-im-netz-gpt
    ```

### Usage

To use the API, make requests to the following endpoint:

- Get a specific section of the BGB:
    ```bash
    curl -X 'GET' \
      'http://localhost:8000/bgb/§1' \
      -H 'accept: application/json'
    ```
