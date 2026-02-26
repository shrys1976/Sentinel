import { type FormEvent, useState } from "react";

export default function Contact() {
  const [submitted, setSubmitted] = useState(false);

  const onSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setSubmitted(true);
  };

  return (
    <section className="min-h-screen bg-[linear-gradient(180deg,#020202_0%,#040917_52%,#020202_100%)] px-5 py-28 text-slate-100 md:px-8">
      <div className="mx-auto w-full max-w-3xl rounded-2xl border border-white/10 bg-slate-950/60 p-8 backdrop-blur-sm">
        <h1 className="instrument-serif-regular text-5xl tracking-tight md:text-6xl">Contact</h1>
        <p className="mt-4 text-slate-300">
          Share your query and the Sentinel team will get back to you.
        </p>

        <form onSubmit={onSubmit} className="mt-8 space-y-5">
          <div className="grid gap-5 md:grid-cols-2">
            <div>
              <label htmlFor="firstName" className="mb-2 block text-sm text-slate-300">
                First Name
              </label>
              <input
                id="firstName"
                name="firstName"
                required
                className="w-full rounded-xl border border-white/15 bg-black/40 px-4 py-3 text-slate-100 outline-none transition focus:border-white/40"
              />
            </div>
            <div>
              <label htmlFor="lastName" className="mb-2 block text-sm text-slate-300">
                Last Name
              </label>
              <input
                id="lastName"
                name="lastName"
                required
                className="w-full rounded-xl border border-white/15 bg-black/40 px-4 py-3 text-slate-100 outline-none transition focus:border-white/40"
              />
            </div>
          </div>

          <div>
            <label htmlFor="email" className="mb-2 block text-sm text-slate-300">
              Email
            </label>
            <input
              id="email"
              name="email"
              type="email"
              required
              className="w-full rounded-xl border border-white/15 bg-black/40 px-4 py-3 text-slate-100 outline-none transition focus:border-white/40"
            />
          </div>

          <div>
            <label htmlFor="message" className="mb-2 block text-sm text-slate-300">
              Message
            </label>
            <textarea
              id="message"
              name="message"
              required
              rows={6}
              className="w-full rounded-xl border border-white/15 bg-black/40 px-4 py-3 text-slate-100 outline-none transition focus:border-white/40"
            />
          </div>

          <button
            type="submit"
            className="rounded-xl bg-slate-200 px-6 py-3 text-sm font-extrabold uppercase tracking-[0.08em] text-black transition hover:bg-white"
          >
            Submit Message
          </button>
        </form>

        {submitted ? (
          <p className="mt-5 text-sm text-emerald-300">
            Message submitted successfully. We will contact you soon.
          </p>
        ) : null}
      </div>
    </section>
  );
}
