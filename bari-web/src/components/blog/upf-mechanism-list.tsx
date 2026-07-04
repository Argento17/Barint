type MechItem = { id: string; title: string; text: string };

/**
 * The 3-item mechanism breakdown ("מייצבים" / "שומן" / "NOVA כאחד מכמה אותות")
 * from the "איך בארי מנקדת מוצרים בפועל" section, ported verbatim. Mirrors
 * the owner-approved infographic spec's `.mech .item` card list.
 */
export function UpfMechanismList({ lead, items }: { lead: string; items: MechItem[] }) {
  return (
    <div dir="rtl">
      <p className="mb-3 text-base font-semibold text-[#111318] md:text-lg">{lead}</p>
      <div className="flex flex-col gap-3.5">
        {items.map((item) => (
          <div key={item.id} className="rounded-[0.9rem] border border-black/[0.07] bg-[#FFFFFF] px-5 py-4">
            <p className="mb-1.5 text-[15px] font-extrabold text-[#111318]">{item.title}</p>
            <p className="text-[15px] leading-[1.7] text-[#4E5663]">{item.text}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
