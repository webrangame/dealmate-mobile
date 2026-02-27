# Go Examples: Generate LiteLLM Virtual Key

Complete Go code examples for generating LiteLLM virtual keys.

## Quick Start Example

```go
package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
)

func main() {
	// Configuration
	litellmURL := "https://swzissb82u.us-east-1.awsapprunner.com"
	masterKey := "sk-dcb0c8a73a664a2307b8e2f12ef90a34819204105f32f51cc8c621ebf88c7642"
	userID := "7"

	// Prepare request body
	requestBody := map[string]interface{}{
		"user_id":  userID,
		"duration": nil, // nil = no expiration
	}

	jsonData, err := json.Marshal(requestBody)
	if err != nil {
		fmt.Printf("Error: %v\n", err)
		return
	}

	// Create HTTP request
	url := fmt.Sprintf("%s/key/generate", litellmURL)
	req, err := http.NewRequest("POST", url, bytes.NewBuffer(jsonData))
	if err != nil {
		fmt.Printf("Error: %v\n", err)
		return
	}

	// Set headers
	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("x-litellm-api-key", masterKey)

	// Make request
	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		fmt.Printf("Error: %v\n", err)
		return
	}
	defer resp.Body.Close()

	// Read response
	body, err := io.ReadAll(resp.Body)
	if err != nil {
		fmt.Printf("Error: %v\n", err)
		return
	}

	// Parse response
	var result map[string]interface{}
	json.Unmarshal(body, &result)

	fmt.Printf("Virtual Key: %s\n", result["key"])
}
```

## Complete Example with Error Handling

See `generate-key-go-simple.go` for a complete example with proper error handling.

## HTTP Handler Example

For use in a Go web server/API:

```go
package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"os"
)

const LITELLM_API_URL = "https://swzissb82u.us-east-1.awsapprunner.com"

func getMasterKey() string {
	key := os.Getenv("LITELLM_MASTER_KEY")
	if key == "" {
		key = os.Getenv("LITELLM_API_KEY")
	}
	if key == "" {
		key = "sk-dcb0c8a73a664a2307b8e2f12ef90a34819204105f32f51cc8c621ebf88c7642"
	}
	return key
}

type GenerateKeyRequest struct {
	UserID   string  `json:"user_id"`
	KeyAlias *string `json:"key_alias,omitempty"`
}

type GenerateKeyResponse struct {
	Key      string  `json:"key"`
	UserID   string  `json:"user_id"`
	KeyAlias *string `json:"key_alias,omitempty"`
	Expires  *string `json:"expires,omitempty"`
}

func generateKeyHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	var req GenerateKeyRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, "Invalid request", http.StatusBadRequest)
		return
	}

	if req.UserID == "" {
		http.Error(w, "user_id is required", http.StatusBadRequest)
		return
	}

	// Generate key
	keyResp, err := generateKeyFromLiteLLM(req.UserID, req.KeyAlias)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(keyResp)
}

func generateKeyFromLiteLLM(userID string, keyAlias *string) (*GenerateKeyResponse, error) {
	reqBody := map[string]interface{}{
		"user_id":  userID,
		"duration": nil,
	}
	if keyAlias != nil {
		reqBody["key_alias"] = *keyAlias
	}

	jsonData, _ := json.Marshal(reqBody)
	url := fmt.Sprintf("%s/key/generate", LITELLM_API_URL)
	req, _ := http.NewRequest("POST", url, bytes.NewBuffer(jsonData))

	masterKey := getMasterKey()
	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("x-litellm-api-key", masterKey)

	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	body, _ := io.ReadAll(resp.Body)
	var keyResp GenerateKeyResponse
	json.Unmarshal(body, &keyResp)

	return &keyResp, nil
}

func main() {
	http.HandleFunc("/api/generate-key", generateKeyHandler)
	http.ListenAndServe(":8080", nil)
}
```

## Usage

### Run Simple Example

```bash
go run generate-key-go-simple.go
```

### Run HTTP Handler

```bash
go run generate-key-go-handler.go
# Then make a POST request:
curl -X POST http://localhost:8080/api/generate-key \
  -H "Content-Type: application/json" \
  -d '{"user_id": "7"}'
```

## Environment Variables

Set these in your environment:

```bash
export LITELLM_MASTER_KEY="sk-dcb0c8a73a664a2307b8e2f12ef90a34819204105f32f51cc8c621ebf88c7642"
# OR
export LITELLM_API_KEY="sk-dcb0c8a73a664a2307b8e2f12ef90a34819204105f32f51cc8c621ebf88c7642"
```

## Response Format

```json
{
  "key": "sk-N00S6nZMl_1xqzIZ13mdpw",
  "user_id": "7",
  "key_alias": null,
  "tpm_limit": 100000,
  "rpm_limit": 100,
  "expires": null
}
```

## Error Handling

The API may return errors in this format:

```json
{
  "error": {
    "message": "Error message",
    "type": "auth_error",
    "code": "401"
  }
}
```

Make sure to check `resp.StatusCode` and handle errors appropriately.
