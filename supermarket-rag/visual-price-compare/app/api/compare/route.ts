import { NextRequest, NextResponse } from 'next/server';
import { exec } from 'child_process';
import { promisify } from 'util';
import path from 'path';

const execAsync = promisify(exec);

export async function POST(req: NextRequest) {
    try {
        const { prompt, query } = await req.json();
        const finalPrompt = prompt || query;

        if (!finalPrompt) {
            return NextResponse.json({ error: 'Prompt is required' }, { status: 400 });
        }

        const scriptPath = path.join(process.cwd(), 'compare_prices.py');
        const venvPython = path.join(process.cwd(), 'venv', 'bin', 'python3');

        console.log(`Executing agentic comparison for prompt: ${finalPrompt}`);

        // Execute the python script
        const { stdout, stderr } = await execAsync(`${venvPython} ${scriptPath} --prompt "${finalPrompt.replace(/"/g, '\\"')}"`);

        if (stderr && !stdout) {
            console.error(`Script error: ${stderr}`);
            return NextResponse.json({ error: 'Failed to run comparison script' }, { status: 500 });
        }

        try {
            const results = JSON.parse(stdout);
            return NextResponse.json(results);
        } catch (parseError) {
            console.error(`Parse error: ${parseError}, stdout: ${stdout}`);
            return NextResponse.json({ error: 'Failed to parse script output', details: stdout }, { status: 500 });
        }
    } catch (error: any) {
        console.error(`API Error: ${error.message}`);
        return NextResponse.json({ error: error.message }, { status: 500 });
    }
}
