package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"os"
)

const (
	LITELLM_API_URL = "https://swzissb82u.us-east-1.awsapprunner.com"
	MASTER_KEY      = "sk-dcb0c8a73a664a2307b8e2f12ef90a34819204105f32f51cc8c621ebf88c7642"
)

// GenerateKeyRequest represents the request body for generating a key
type GenerateKeyRequest struct {
	UserID    string  `json:"user_id"`
	Duration  *string `json:"duration,omitempty"` // null for no expiration
	KeyAlias  *string `json:"key_alias,omitempty"`
	TPMLimit  *int    `json:"tpm_limit,omitempty"`
	RPMLimit  *int    `json:"rpm_limit,omitempty"`
}

// GenerateKeyResponse represents the response from LiteLLM
type GenerateKeyResponse struct {
	Key       string  `json:"key"`
	UserID    string  `json:"user_id"`
	KeyAlias  *string `json:"key_alias,omitempty"`
	TPMLimit  *int    `json:"tpm_limit,omitempty"`
	RPMLimit  *int    `json:"rpm_limit,omitempty"`
	Expires   *string `json:"expires,omitempty"`
}

// LiteLLMError represents an error response from LiteLLM
type LiteLLMError struct {
	Error struct {
		Message string `json:"message"`
		Type    string `json:"type"`
		Code    string `json:"code"`
	} `json:"error"`
}

// GenerateVirtualKey generates a new virtual key for a user
func GenerateVirtualKey(userID string, keyAlias *string) (*GenerateKeyResponse, error) {
	// Prepare request body
	reqBody := GenerateKeyRequest{
		UserID:   userID,
		Duration: nil, // nil means no expiration
	}

	if keyAlias != nil {
		reqBody.KeyAlias = keyAlias
	}

	// Marshal request body to JSON
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
	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("x-litellm-api-key", MASTER_KEY)
	req.Header.Set("accept", "application/json")

	// Make HTTP request
	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		return nil, fmt.Errorf("failed to make request: %w", err)
	}
	defer resp.Body.Close()

	// Read response body
	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return nil, fmt.Errorf("failed to read response: %w", err)
	}

	// Check for errors
	if resp.StatusCode != http.StatusOK {
		var litellmErr LiteLLMError
		if err := json.Unmarshal(body, &litellmErr); err == nil {
			return nil, fmt.Errorf("LiteLLM API error: %s (code: %s)", litellmErr.Error.Message, litellmErr.Error.Code)
		}
		return nil, fmt.Errorf("API request failed with status %d: %s", resp.StatusCode, string(body))
	}

	// Parse successful response
	var keyResp GenerateKeyResponse
	if err := json.Unmarshal(body, &keyResp); err != nil {
		return nil, fmt.Errorf("failed to parse response: %w", err)
	}

	return &keyResp, nil
}

func main() {
	// Generate key for user_id=7
	userID := "7"
	keyAlias := "API Key for User 7" // Optional

	fmt.Printf("Generating virtual key for user_id=%s...\n", userID)

	keyResp, err := GenerateVirtualKey(userID, &keyAlias)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error: %v\n", err)
		os.Exit(1)
	}

	// Print results
	fmt.Println("\n✅ Virtual Key Generated Successfully!")
	fmt.Printf("User ID: %s\n", keyResp.UserID)
	fmt.Printf("Virtual Key: %s\n", keyResp.Key)
	if keyResp.KeyAlias != nil {
		fmt.Printf("Key Alias: %s\n", *keyResp.KeyAlias)
	}
	if keyResp.TPMLimit != nil {
		fmt.Printf("TPM Limit: %d\n", *keyResp.TPMLimit)
	}
	if keyResp.RPMLimit != nil {
		fmt.Printf("RPM Limit: %d\n", *keyResp.RPMLimit)
	}
	if keyResp.Expires != nil {
		fmt.Printf("Expires: %s\n", *keyResp.Expires)
	} else {
		fmt.Println("Expires: Never")
	}
}
