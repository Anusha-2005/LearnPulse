import { Logo } from "@/components/Logo";

export default function AuthLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    return (
        <div className="min-h-screen grid lg:grid-cols-2">
            {/* Left: Branding & Visual */}
            {/* Left: Branding & Visual */}
            <div className="hidden lg:flex flex-col bg-black text-white p-12 relative overflow-hidden login-left">
                {/* Logo */}
                <div className="z-10">
                    <Logo variant="dark" />
                </div>

                {/* Centered Hero Content */}
                <div className="flex-1 flex flex-col justify-center z-10 max-w-lg">
                    <h1 className="text-5xl font-bold leading-tight mb-6">Act Early, Help Better.</h1>
                        <p className="text-gray-400 text-xl leading-relaxed">
                            LearnPulse — an adaptive student‑success platform powered by ML. We surface early warning signals, recommend timely, personalized interventions, and help educators turn risk into opportunity.
                        </p>
                </div>

                {/* Abstract Pattern */}
                <div className="absolute top-0 right-0 w-[600px] h-[600px] bg-blue-900/20 rounded-full blur-3xl -translate-y-1/2 translate-x-1/2"></div>
                <div className="absolute bottom-0 left-0 w-[600px] h-[600px] bg-purple-900/20 rounded-full blur-3xl translate-y-1/2 -translate-x-1/2"></div>

                <div className="z-10 text-sm text-gray-500">
                    © 2026 LearnPulse — Empowering educators, one student at a time.
                </div>
            </div>

            {/* Right: Auth Form */}
            <div className="flex items-center justify-center p-8 bg-gray-50">
                <div className="w-full max-w-md space-y-8 login-wrapper">
                    {children}
                </div>
            </div>
        </div>
    );
}
