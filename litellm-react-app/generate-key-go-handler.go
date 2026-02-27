package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
)

const (
	LITELLM_API_URL = "https://swzissb82u.us-east-1.awsapprunner.com"
)

// Get master key from environment variable or use default
func getMasterKey() string {
	key := os.Getenv("LITELLM_MASTER_KEY")
	if key == "" {
		key = os.Getenv("LITELLM_API_KEY")
	}
	if key == "" {
		// Fallback to default (not recommended for production)
		key = "sk-dcb0c8a73a664a2307b8e2f12ef90a34819204105f32f51cc8c621ebf88c7642"
	}
	return key
}

// GenerateKeyRequest represents the request body
type GenerateKeyRequest struct {
	UserID   string  `json:"user_id"`
	Duration *string `json:"duration,omitempty"`
	KeyAlias *string `json:"key_alias,omitempty"`
}

// GenerateKeyResponse represents the response
type GenerateKeyResponse struct {
	Key      string  `json:"key"`
	UserID   string  `json:"user_id"`
	KeyAlias *string `json:"key_alias,omitempty"`
	Expires  *string `json:"expires,omitempty"`
}

// ErrorResponse represents an error response
type ErrorResponse struct {
	Error string `json:"error"`
}

// generateKeyHandler handles HTTP requests to generate a virtual key
func generateKeyHandler(w http.ResponseWriter, r *http.Request) {
	// Only allow POST requests
	if r.Method != http.MethodPost {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	// Parse request body
	var req GenerateKeyRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		respondWithError(w, http.StatusBadRequest, "Invalid request body: "+err.Error())
		return
	}

	// Validate user_id
	if req.UserID == "" {
		respondWithError(w, http.StatusBadRequest, "user_id is required")
		return
	}

	// Generate the key using LiteLLM API
	keyResp, err := generateVirtualKeyFromLiteLLM(req.UserID, req.KeyAlias)
	if err != nil {
		log.Printf("Error generating key for user_id=%s: %v", req.UserID, err)
		respondWithError(w, http.StatusInternalServerError, "Failed to generate key: "+err.Error())
		return
	}

	// Return success response
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	json.NewEncoder(w).Encode(keyResp)
}

// generateVirtualKeyFromLiteLLM calls LiteLLM API to generate a key
func generateVirtualKeyFromLiteLLM(userID string, keyAlias *string) (*GenerateKeyResponse, error) {
	// Prepare request
	reqBody := map[string]interface{}{
		"user_id":  userID,
		"duration": nil,
	}
	if keyAlias != nil {
		reqBody["key_alias"] = *keyAlias
	}

	jsonData, err := json.Marshal(reqBody)
	if err != nil {
		return nil, fmt.Errorf("failed to marshal request: %w", err)
	}

	// Create HTTP request
	url := fmt.Sprintf("%s/key/generate", LITELLM_API_URL)
	req, err := http.NewRequest("POST", url, bytes.NewBuffer(jsonData))
	if err != nil {
		return nil, fmt.Errorf("failed to create request: %w", err)
	}

	// Set headers
	masterKey := getMasterKey()
	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("x-litellm-api-key", masterKey)
	req.Header.Set("accept", "application/json")

	// Make request
	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		return nil, fmt.Errorf("failed to make request: %w", err)
	}
	defer resp.Body.Close()

	// Read response
	var keyResp GenerateKeyResponse
	if err := json.NewDecoder(resp.Body).Decode(&keyResp); err != nil {
		return nil, fmt.Errorf("failed to parse response: %w", err)
	}

	if resp.StatusCode != http.StatusOK {
		return nil, fmt.Errorf("LiteLLM API returned status %d", resp.StatusCode)
	}

	return &keyResp, nil
}

// respondWithError sends an error response
func respondWithError(w http.ResponseWriter, code int, message string) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(code)
	json.NewEncoder(w).Encode(ErrorResponse{Error: message})
}

func main() {
	// Example: HTTP handler
	http.HandleFunc("/api/generate-key", generateKeyHandler)

	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}

	log.Printf("Server starting on port %s", port)
	log.Fatal(http.ListenAndServe(":"+port, nil))
}
