"use client";

import { useState, useRef, useEffect } from "react";

type Citation = {
  url: string;
  date: string;
};

type Message = {
  role: "user" | "assistant";
  content: string;
  citations?: Citation[];
  isLoading?: boolean;
};

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage: Message = { role: "user", content: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");

    // Add temporary loading message
    const loadingMessage: Message = { role: "assistant", content: "", isLoading: true };
    setMessages((prev) => [...prev, loadingMessage]);

    try {
      const response = await fetch("http://localhost:8000/api/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ question: userMessage.content }),
      });

      if (!response.ok) {
        throw new Error("Failed to fetch response");
      }

      const data = await response.json();
      
      setMessages((prev) => {
        // Remove the loading message and add the real one
        const updated = prev.filter((msg) => !msg.isLoading);
        return [...updated, { role: "assistant", content: data.answer, citations: data.citations }];
      });
    } catch (error) {
      console.error(error);
      setMessages((prev) => {
        const updated = prev.filter((msg) => !msg.isLoading);
        return [...updated, { role: "assistant", content: "Sorry, there was an error processing your request." }];
      });
    }
  };

  return (
    <>
      {/* TopAppBar */}
      <header className="bg-surface/80 dark:bg-surface/80 backdrop-blur-xl fixed top-0 w-full z-50 border-b border-white/10 shadow-sm flex items-center justify-between px-margin-mobile md:px-margin-desktop h-16">
        <button
          aria-label="Open Menu"
          className="text-on-surface-variant hover:opacity-80 transition-opacity active:scale-95 md:hidden"
          onClick={() => setIsSidebarOpen(!isSidebarOpen)}
        >
          <span className="material-symbols-outlined">menu</span>
        </button>
        <div className="font-headline-md text-headline-md text-primary font-bold ml-4 md:ml-0 flex-1 md:text-left text-center">
          HDFC AI Assistant
        </div>
        <div className="w-10 h-10 rounded-full bg-surface-variant flex items-center justify-center overflow-hidden border border-white/10">
          <img
            alt="User Profile"
            className="w-full h-full object-cover"
            src="https://lh3.googleusercontent.com/aida-public/AB6AXuBvbfOK3m8aJbM4i2KQO-lq9rhXTrJoV4PbGqjsUxxP7Z4pKmYk5ViIetozeXdKmeUY-XvF2qpiQqI7h7ZabwlKcgOTFGrEyFMJYO7UpblJd6gyKdS3u8vXjoXG5KGSlSkir3CqBaWpwui4X6xGDdmbmCDPkc6KM86NRXmdynCHLmDU9C2eX2LIrG_5CxmeqtHcEywxgF8B_Gs0nMquhU5qcXKXgkfCeSL3b-AZugE74SZtCIhECg_jnA"
          />
        </div>
      </header>

      {/* NavigationDrawer (Mobile / Tablet) */}
      <nav
        className={`bg-surface-container dark:bg-surface-container-low/90 backdrop-blur-2xl h-screen w-80 fixed left-0 top-0 z-40 border-r border-white/10 shadow-2xl flex flex-col p-4 gap-2 transition-transform duration-300 ease-in-out pt-20 ${
          isSidebarOpen ? "translate-x-0" : "-translate-x-full md:translate-x-0"
        }`}
      >
        <div className="font-headline-md text-headline-md text-primary mb-6 mt-4 pl-2">
          HDFC Funds
        </div>
        <div className="flex-1 overflow-y-auto chat-scroll flex flex-col gap-1">
          {[
            { icon: "trending_up", text: "HDFC Top 100 Fund" },
            { icon: "analytics", text: "HDFC Mid-Cap Opportunities" },
            { icon: "monitoring", text: "HDFC Small Cap Fund" },
            { icon: "balance", text: "HDFC Balanced Advantage" },
            { icon: "account_balance_wallet", text: "HDFC Flexi Cap Fund" },
            { icon: "water_drop", text: "HDFC Liquid Fund" },
            { icon: "security", text: "HDFC Corporate Bond" },
            { icon: "cloud_download", text: "HDFC Index Nifty 50" },
            { icon: "cloud_upload", text: "HDFC TaxSaver" },
          ].map((item, index) => (
            <a
              key={index}
              className="text-on-surface-variant hover:bg-surface-variant/50 rounded-lg hover:bg-white/5 transition-colors p-3 flex items-center gap-3"
              href="#"
            >
              <span className="material-symbols-outlined">{item.icon}</span>
              <span className="font-body-md text-body-md">{item.text}</span>
            </a>
          ))}
        </div>
        <div className="mt-auto pt-4 border-t border-white/10 flex items-center gap-3 p-3">
          <div className="w-2 h-2 rounded-full bg-primary animate-pulse"></div>
          <span className="font-label-sm text-label-sm text-on-surface-variant">
            Data Freshness: Live
          </span>
        </div>
      </nav>

      {/* Main Content Area */}
      <main className="flex-1 flex flex-col md:ml-80 pt-16 pb-[100px] h-screen relative overflow-hidden">
        <div
          className="absolute inset-0 z-0 pointer-events-none opacity-20"
          style={{
            backgroundImage:
              "radial-gradient(circle at 50% 50%, rgba(74, 222, 128, 0.1) 0%, transparent 50%)",
          }}
        ></div>
        <div className="flex-1 overflow-y-auto p-margin-mobile md:p-margin-desktop flex flex-col gap-8 chat-scroll z-10 w-full max-w-container-max mx-auto relative">
          
          {messages.length === 0 ? (
            <div className="flex flex-col items-center justify-center min-h-[50vh] text-center my-auto">
              <h1 className="font-display-lg-mobile md:font-display-lg text-display-lg-mobile md:text-display-lg text-on-surface mb-8 bg-clip-text text-transparent bg-gradient-to-r from-on-surface to-on-surface-variant">
                Ask anything about <br /> HDFC Mutual Funds
              </h1>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 w-full max-w-4xl">
                <button onClick={() => setInput("What is the current AUM and 1-year return for the HDFC Small Cap Fund?")} className="glass-panel rounded-xl p-6 text-left hover:bg-white/5 transition-all group relative overflow-hidden border border-white/10 hover:border-primary/30">
                  <div className="absolute inset-0 bg-gradient-to-br from-primary/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
                  <span className="material-symbols-outlined text-primary mb-3 block">monitoring</span>
                  <h3 className="font-body-md text-body-md text-on-surface font-semibold mb-1">AUM of HDFC Small Cap</h3>
                  <p className="font-label-sm text-label-sm text-on-surface-variant">Check latest asset under management data.</p>
                </button>
                <button onClick={() => setInput("Compare the exit loads across different HDFC funds")} className="glass-panel rounded-xl p-6 text-left hover:bg-white/5 transition-all group relative overflow-hidden border border-white/10 hover:border-secondary/30">
                  <div className="absolute inset-0 bg-gradient-to-br from-secondary/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
                  <span className="material-symbols-outlined text-secondary mb-3 block">compare_arrows</span>
                  <h3 className="font-body-md text-body-md text-on-surface font-semibold mb-1">Compare exit loads</h3>
                  <p className="font-label-sm text-label-sm text-on-surface-variant">Analyze fees across different fund categories.</p>
                </button>
                <button onClick={() => setInput("Who are the fund managers for the Top 100 fund?")} className="glass-panel rounded-xl p-6 text-left hover:bg-white/5 transition-all group relative overflow-hidden border border-white/10 hover:border-tertiary/30">
                  <div className="absolute inset-0 bg-gradient-to-br from-tertiary/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
                  <span className="material-symbols-outlined text-tertiary mb-3 block">group</span>
                  <h3 className="font-body-md text-body-md text-on-surface font-semibold mb-1">Fund managers</h3>
                  <p className="font-label-sm text-label-sm text-on-surface-variant">Learn who is managing the top performing funds.</p>
                </button>
              </div>
            </div>
          ) : (
            <div className="flex flex-col gap-6 mt-auto">
              {messages.map((msg, idx) => (
                <div key={idx} className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}>
                  {msg.role === "user" ? (
                    <div className="bg-surface-variant text-on-surface p-4 rounded-2xl rounded-tr-sm max-w-[85%] md:max-w-[70%] font-body-md text-body-md shadow-sm border border-white/5">
                      {msg.content}
                    </div>
                  ) : (
                    <div className={`glass-panel p-5 rounded-2xl rounded-tl-sm max-w-[90%] md:max-w-[75%] font-body-md text-body-md relative overflow-hidden ${msg.isLoading ? 'w-24 flex items-center justify-center p-4' : ''}`}>
                      {!msg.isLoading && <div className="absolute top-0 left-0 w-1 h-full bg-primary"></div>}
                      
                      {msg.isLoading ? (
                        <div className="typing-indicator flex items-center h-5">
                          <span></span><span></span><span></span>
                        </div>
                      ) : (
                        <>
                          <div className="mb-4 text-on-surface leading-relaxed whitespace-pre-wrap">
                            {msg.content}
                          </div>
                          
                          {/* Citations */}
                          {msg.citations && msg.citations.length > 0 && (
                            <div className="flex flex-wrap gap-2 mt-4 pt-4 border-t border-white/10">
                              {msg.citations.map((cite, i) => (
                                <a
                                  key={i}
                                  href={cite.url}
                                  target="_blank"
                                  rel="noopener noreferrer"
                                  className="bg-surface-container-high hover:bg-surface-variant transition-colors border border-outline/30 rounded-full px-3 py-1 font-label-sm text-label-sm text-on-surface-variant flex items-center gap-1"
                                >
                                  <span className="material-symbols-outlined" style={{ fontSize: "14px" }}>
                                    description
                                  </span>
                                  [Source: {cite.url.split('/').pop()?.replace('.html', '') || 'Link'}, Data: {cite.date}]
                                </a>
                              ))}
                            </div>
                          )}
                        </>
                      )}
                    </div>
                  )}
                </div>
              ))}
              <div ref={messagesEndRef} />
            </div>
          )}
        </div>

        {/* Input Area */}
        <div className="absolute bottom-0 left-0 w-full bg-gradient-to-t from-background via-background/90 to-transparent pt-10 pb-6 px-margin-mobile md:px-margin-desktop z-20">
          <div className="max-w-4xl mx-auto relative">
            <div className="absolute inset-0 bg-primary/5 blur-xl rounded-full pointer-events-none"></div>
            <form
              onSubmit={handleSubmit}
              className="glass-panel rounded-full p-2 flex items-center gap-2 border border-white/20 focus-within:border-primary/50 focus-within:shadow-[0_0_20px_rgba(74,222,128,0.15)] transition-all duration-300 relative z-10 bg-surface-container-low/80"
            >
              <button
                type="button"
                className="w-10 h-10 rounded-full flex items-center justify-center text-on-surface-variant hover:text-on-surface hover:bg-white/5 transition-colors ml-1"
              >
                <span className="material-symbols-outlined">attach_file</span>
              </button>
              <input
                value={input}
                onChange={(e) => setInput(e.target.value)}
                className="flex-1 bg-transparent border-none text-on-surface focus:ring-0 placeholder:text-on-surface-variant/50 font-body-md text-body-md px-2 py-3 outline-none"
                placeholder="Ask about funds, performance, or strategy..."
                type="text"
              />
              <button
                type="submit"
                disabled={!input.trim()}
                className="w-10 h-10 rounded-full bg-primary text-on-primary flex items-center justify-center hover:bg-primary-fixed transition-colors mr-1 shadow-sm disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <span
                  className="material-symbols-outlined"
                  style={{ fontVariationSettings: "'FILL' 1" }}
                >
                  send
                </span>
              </button>
            </form>
            <div className="text-center mt-3">
              <span className="font-label-sm text-label-sm text-on-surface-variant/50">
                AI suggestions are based on historical data. Not financial advice.
              </span>
            </div>
          </div>
        </div>
      </main>
    </>
  );
}
