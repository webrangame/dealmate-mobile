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
		fmt.Printf("Error marshaling JSON: %v\n", err)
		return
	}

	// Create HTTP request
	url := fmt.Sprintf("%s/key/generate", litellmURL)
	req, err := http.NewRequest("POST", url, bytes.NewBuffer(jsonData))
	if err != nil {
		fmt.Printf("Error creating request: %v\n", err)
		return
	}

	// Set headers
	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("x-litellm-api-key", masterKey)
	req.Header.Set("accept", "application/json")

	// Make request
	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		fmt.Printf("Error making request: %v\n", err)
		return
	}
	defer resp.Body.Close()

	// Read response
	body, err := io.ReadAll(resp.Body)
	if err != nil {
		fmt.Printf("Error reading response: %v\n", err)
		return
	}

	// Check status code
	if resp.StatusCode != http.StatusOK {
		fmt.Printf("API Error (Status %d): %s\n", resp.StatusCode, string(body))
		return
	}

	// Parse response
	var result map[string]interface{}
	if err := json.Unmarshal(body, &result); err != nil {
		fmt.Printf("Error parsing response: %v\n", err)
		fmt.Printf("Raw response: %s\n", string(body))
		return
	}

	// Print results
	fmt.Println("✅ Virtual Key Generated Successfully!")
	fmt.Printf("User ID: %s\n", result["user_id"])
	fmt.Printf("Virtual Key: %s\n", result["key"])
	
	if result["key_alias"] != nil {
		fmt.Printf("Key Alias: %v\n", result["key_alias"])
	}
	if result["expires"] == nil {
		fmt.Println("Expires: Never")
	} else {
		fmt.Printf("Expires: %v\n", result["expires"])
	}
}
