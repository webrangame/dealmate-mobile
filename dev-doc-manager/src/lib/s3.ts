import { S3Client, PutObjectCommand, GetObjectCommand } from "@aws-sdk/client-s3";
import { getSignedUrl } from "@aws-sdk/s3-request-presigner";

const s3Client = new S3Client({
    region: process.env.AWS_REGION || "us-east-1",
    credentials: {
        accessKeyId: process.env.AWS_ACCESS_KEY_ID || "",
        secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY || "",
    },
});

export const getPresignedUploadUrl = async (fileName: string, contentType: string) => {
    const bucket = process.env.S3_BUCKET_NAME || process.env.AWS_S3_BUCKET;
    const path = process.env.AWS_S3_PATH || "backend";
    const key = `${path}/${Date.now()}-${fileName}`;
    const kmsKeyId = process.env.AWS_KMS_KEY_ID;

    const command = new PutObjectCommand({
        Bucket: bucket,
        Key: key,
        ContentType: contentType,
        ...(kmsKeyId ? {
            ServerSideEncryption: "aws:kms",
            SSEKMSKeyId: kmsKeyId,
        } : {}),
    });

    const url = await getSignedUrl(s3Client, command, { expiresIn: 3600 });
    return { url, key };
};

export const uploadFileServerSide = async (file: Buffer, fileName: string, contentType: string) => {
    const bucket = process.env.S3_BUCKET_NAME || process.env.AWS_S3_BUCKET || "officedoc";
    const path = process.env.AWS_S3_PATH || "backend";
    const key = `${path}/${Date.now()}-${fileName}`;
    const kmsKeyId = process.env.AWS_KMS_KEY_ID;

    try {
        console.log(`Starting server-side upload for ${fileName} to bucket ${bucket}`);
        const command = new PutObjectCommand({
            Bucket: bucket,
            Key: key,
            Body: file,
            ContentType: contentType,
            ...(kmsKeyId ? {
                ServerSideEncryption: "aws:kms",
                SSEKMSKeyId: kmsKeyId,
            } : {}),
        });

        await s3Client.send(command);
        console.log(`Upload successful for ${key}`);
        return { key, url: getFileUrl(key) };
    } catch (error: any) {
        console.error("AWS S3 Upload Error:", {
            message: error.message,
            code: error.code,
            bucket,
            key,
            kmsKeyId
        });
        throw error;
    }
};

export const getPresignedViewUrl = async (key: string) => {
    const bucket = process.env.S3_BUCKET_NAME || process.env.AWS_S3_BUCKET || "dev-doc-manager-storage-582604091763";

    const command = new GetObjectCommand({
        Bucket: bucket,
        Key: key,
    });

    return await getSignedUrl(s3Client, command, { expiresIn: 3600 });
};

export const getFileUrl = (key: string) => {
    const bucket = process.env.S3_BUCKET_NAME || process.env.AWS_S3_BUCKET;
    const region = process.env.AWS_REGION || "us-east-1";
    return `https://${bucket}.s3.${region}.amazonaws.com/${key}`;
};
