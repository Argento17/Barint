import { NextResponse } from "next/server";

import { isAuthed, isConfigured } from "@/lib/admin/auth";
import { githubConfigured } from "@/lib/admin/github";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

export async function GET() {
  return NextResponse.json({
    authed: await isAuthed(),
    loginConfigured: isConfigured(),
    githubConfigured: githubConfigured(),
  });
}
