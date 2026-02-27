import { NextRequest, NextResponse } from "next/server";
import { prisma } from "@/lib/prisma";
import { getPresignedViewUrl } from "@/lib/s3";
import { DocumentType } from "@prisma/client";

export async function GET(req: NextRequest) {
    try {
        const { searchParams } = new URL(req.url);
        const type = searchParams.get("type") as DocumentType | null;

        const documents = await prisma.document.findMany({
            where: type ? { type } : {},
            orderBy: { createdAt: "desc" },
        });

        // Generate presigned URLs for documents with a fileKey
        const docsWithPresignedUrls = await Promise.all(
            (documents as any[]).map(async (doc: any) => {
                if (doc.fileKey) {
                    try {
                        const presignedUrl = await getPresignedViewUrl(doc.fileKey);
                        return { ...doc, fileUrl: presignedUrl };
                    } catch (error) {
                        console.error(`Failed to generate presigned URL for doc ${doc.id}:`, error);
                        return doc;
                    }
                }
                return doc;
            })
        );

        return NextResponse.json(docsWithPresignedUrls);
    } catch (error) {
        console.error("Failed to fetch documents:", error);
        return NextResponse.json({ error: "Failed to fetch documents" }, { status: 500 });
    }
}

export async function POST(req: NextRequest) {
    try {
        const body = await req.json();
        const { title, type, content, fileUrl, fileKey, externalLink } = body;

        if (!title || !type) {
            return NextResponse.json({ error: "Title and type are required" }, { status: 400 });
        }

        const document = await prisma.document.create({
            data: {
                title,
                type: type as DocumentType,
                content,
                fileUrl,
                fileKey,
                externalLink,
            } as any,
        });

        return NextResponse.json(document);
    } catch (error) {
        console.error("Failed to create document:", error);
        return NextResponse.json({ error: "Failed to create document" }, { status: 500 });
    }
}
