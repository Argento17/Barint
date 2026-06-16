import { redirect } from "next/navigation";

// Route renamed: /hashvaot/cakes-hard-cookies → /hashvaot/cakes (TASK-283)
// This redirect ensures old links remain functional.
export default function CakesHardCookiesRedirect() {
  redirect("/hashvaot/cakes");
}
