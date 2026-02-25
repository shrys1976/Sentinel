import { FormEvent, useMemo, useState } from "react";
import { supabase } from "../lib/supabase";

type LoginProps = {
  onSuccess: () => void;
};

export default function Login({ onSuccess }: LoginProps) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [info, setInfo] = useState<string | null>(null);

  const emailRedirectTo = useMemo(
    () => `${window.location.origin}/login`,
    []
  );

  const submit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setError(null);
    setInfo(null);

    if (!email.trim() || !password.trim()) {
      setError("Email and password are required.");
      return;
    }

    setSubmitting(true);
    try {
      const signIn = await supabase.auth.signInWithPassword({
        email: email.trim(),
        password,
      });

      if (!signIn.error && signIn.data.session) {
        onSuccess();
        return;
      }

      const signInError = signIn.error?.message ?? "Unable to login.";
      if (signInError.toLowerCase().includes("email not confirmed")) {
        setError("Email is not verified. Please confirm your inbox first.");
        return;
      }

      const signUp = await supabase.auth.signUp({
        email: email.trim(),
        password,
        options: { emailRedirectTo },
      });

      if (signUp.error) {
        const msg = signUp.error.message.toLowerCase();
        if (msg.includes("already") || msg.includes("registered")) {
          setError("Incorrect email or password.");
          return;
        }
        setError(signUp.error.message);
        return;
      }

      setInfo("Account created. Check your email to confirm, then login.");
      setTimeout(() => {
        window.location.href = "/login";
      }, 1200);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-black px-5 py-24 text-slate-100">
      <div className="w-full max-w-md rounded-2xl border border-white/10 bg-slate-950/70 p-7 backdrop-blur-sm">
        <h1 className="instrument-serif-regular text-4xl tracking-tight">Login</h1>
        <p className="mt-2 text-sm text-slate-400">
          New email automatically creates an account. Existing email signs in.
        </p>

        <form onSubmit={submit} className="mt-6 space-y-4">
          <label className="block text-sm">
            <span className="mb-1 block text-slate-300">Email</span>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full rounded-xl border border-white/15 bg-black/60 px-3 py-2 text-slate-100 outline-none transition focus:border-white/40"
              placeholder="you@example.com"
              autoComplete="email"
            />
          </label>

          <label className="block text-sm">
            <span className="mb-1 block text-slate-300">Password</span>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full rounded-xl border border-white/15 bg-black/60 px-3 py-2 text-slate-100 outline-none transition focus:border-white/40"
              placeholder="••••••••"
              autoComplete="current-password"
            />
          </label>

          {error ? <p className="text-sm text-rose-300">{error}</p> : null}
          {info ? <p className="text-sm text-emerald-300">{info}</p> : null}

          <button
            type="submit"
            disabled={submitting}
            className="w-full rounded-xl bg-white px-4 py-2 text-sm font-semibold text-black transition hover:bg-slate-200 disabled:cursor-not-allowed disabled:opacity-60"
          >
            {submitting ? "Processing..." : "Continue"}
          </button>
        </form>
      </div>
    </div>
  );
}
