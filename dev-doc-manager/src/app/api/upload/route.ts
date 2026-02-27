import { NextRequest, NextResponse } from "next/server";
import { uploadFileServerSide } from "@/lib/s3";

export async function POST(req: NextRequest) {
    try {
        const formData = await req.formData();
        const file = formData.get("file") as File;

        if (!file) {
            return NextResponse.json({ error: "No file provided" }, { status: 400 });
        }

        const buffer = Buffer.from(await file.arrayBuffer());
        const result = await uploadFileServerSide(buffer, file.name, file.type);

        return NextResponse.json(result);
    } catch (error) {
        console.error("Server-side upload failed:", error);
        return NextResponse.json({ error: "Server-side upload failed" }, { status: 500 });
    }
}
