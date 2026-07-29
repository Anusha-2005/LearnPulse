import { Logo } from "@/components/Logo";

export default function AuthLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    return (
        <div className="min-h-screen grid lg:grid-cols-2 bg-neutral-50 dark:bg-neutral-950 transition-colors duration-300">
            {/* Left: Branding & Visual */}
            <div className="hidden lg:flex flex-col bg-gradient-to-br from-neutral-950 via-slate-900 to-neutral-950 text-white p-16 relative overflow-hidden">
                {/* Logo */}
                <div className="z-10">
                    <Logo variant="dark" className="scale-110 origin-left" />
                </div>

                {/* Centered Hero Content */}
                <div className="flex-1 flex flex-col justify-center z-10 max-w-lg">
                    <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-blue-500/10 border border-blue-500/20 text-blue-400 text-xs font-semibold uppercase tracking-wider mb-6 w-fit">
                        ✨ Machine Learning Powered
                    </div>
                    <h1 className="text-5xl font-bold leading-tight mb-6 tracking-tight">Act Early.<br />Help Better.</h1>
                    <p className="text-slate-400 text-lg leading-relaxed font-medium">
                        LearnPulse is a professional student success dashboard. We parse engagement data, flag warning signals early, and recommend timely, personalized advisor interventions.
                    </p>
                </div>

                {/* Abstract Pattern */}
                <div className="absolute top-0 right-0 w-[600px] h-[600px] bg-blue-900/10 rounded-full blur-[120px] -translate-y-1/2 translate-x-1/2"></div>
                <div className="absolute bottom-0 left-0 w-[600px] h-[600px] bg-indigo-900/15 rounded-full blur-[120px] translate-y-1/2 -translate-x-1/2"></div>

                <div className="z-10 text-xs text-slate-500 font-medium">
                    © 2026 LearnPulse — Dedicated to academic success.
                </div>
            </div>

            {/* Right: Auth Form */}
            <div className="flex items-center justify-center p-8 bg-neutral-50 dark:bg-neutral-950 transition-colors duration-300">
                <div className="w-full max-w-md space-y-6">
                    {children}
                </div>
            </div>
        </div>
    );
}
