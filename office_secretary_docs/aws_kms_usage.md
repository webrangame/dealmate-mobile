# AWS KMS Encryption Example (Node.js)

This guide shows how to encrypt sensitive data (like OAuth tokens) using AWS KMS before storing it in your database, and how to decrypt it when needed.

## 1. Install AWS SDK
First, install the KMS client:
```bash
npm install @aws-sdk/client-kms
```

## 2. Code Example (`kms_utils.js`)

```javascript
/*
 * AWS KMS Encryption/Decryption Utility
 * Uses @aws-sdk/client-kms (v3)
 */

import { KMSClient, EncryptCommand, DecryptCommand } from "@aws-sdk/client-kms";

// Initialize the KMS Client
const client = new KMSClient({ region: "us-east-1" });

// Your KMS Key ID (ARN or Alias)
// Best Practice: Store this in an environment variable
const KMS_KEY_ID = process.env.KMS_KEY_ID || "alias/office-secretary-key";

/**
 * Encrypts a plain text string.
 * Returns a Base64 string to store in your database.
 */
export async function encryptData(plainText) {
  try {
    const command = new EncryptCommand({
      KeyId: KMS_KEY_ID,
      Plaintext: Buffer.from(plainText), // Convert string to Buffer
    });

    const response = await client.send(command);
    
    // AWS returns the CiphertextBlob as a Uint8Array.
    // Convert it to Base64 string for easy storage in Postgres/DynamoDB.
    return Buffer.from(response.CiphertextBlob).toString("base64");
  } catch (error) {
    console.error("Encryption Error:", error);
    throw new Error("Failed to encrypt data");
  }
}

/**
 * Decrypts a Base64 string back to plain text.
 */
export async function decryptData(cipherTextBase64) {
  try {
    const command = new DecryptCommand({
      CiphertextBlob: Buffer.from(cipherTextBase64, "base64"),
    });

    const response = await client.send(command);

    // Convert the returned Uint8Array back to a UTF-8 string
    return Buffer.from(response.Plaintext).toString("utf-8");
  } catch (error) {
    console.error("Decryption Error:", error);
    throw new Error("Failed to decrypt data");
  }
}

// --- Usage Example ---
(async () => {
  const secret = "my-super-secret-oauth-token";
  
  console.log("Original:", secret);
  
  // 1. Encrypt
  const encrypted = await encryptData(secret);
  console.log("Encrypted (Store this in DB):", encrypted);
  
  // 2. Decrypt
  const decrypted = await decryptData(encrypted);
  console.log("Decrypted:", decrypted);
})();
```

## 3. Key Concepts
*   **KeyId**: The unique identifier for your KMS Master Key. You create this in the AWS Console under Key Management Service.
*   **CiphertextBlob**: The raw encrypted bytes returned by AWS. We convert this to `Base64` to store it easily in text fields in your database.
*   **Permissions**: The AWS Role running this code (e.g., your ECS Task Role or Lambda Role) must have `kms:Encrypt` and `kms:Decrypt` permissions for the specified Key ID.
