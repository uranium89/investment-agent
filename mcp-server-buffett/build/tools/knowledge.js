import { z } from "zod";
import { readFileSync, readdirSync, existsSync, writeFileSync, mkdirSync } from "fs";
import { join, resolve } from "path";
// Resolve the Buffett knowledge base directory.
// Priority: BUFFETT_KNOWLEDGE_DIR env var → relative path from built JS file
// (mcp-server-buffett/build/tools/knowledge.js → ../../../knowledge/buffett)
const KNOWLEDGE_DIR = process.env.BUFFETT_KNOWLEDGE_DIR
    ? resolve(process.env.BUFFETT_KNOWLEDGE_DIR)
    : resolve(import.meta.dirname ?? __dirname, "../../../knowledge/buffett");
// Reports directory: knowledge/reports/ (cùng cấp với knowledge/buffett)
const REPORTS_DIR = process.env.REPORTS_DIR
    ? resolve(process.env.REPORTS_DIR)
    : resolve(KNOWLEDGE_DIR, "../reports");
function loadIndex() {
    const indexPath = join(REPORTS_DIR, "index.json");
    if (!existsSync(indexPath))
        return [];
    try {
        return JSON.parse(readFileSync(indexPath, "utf-8"));
    }
    catch {
        return [];
    }
}
function saveIndex(reports) {
    // Sắp xếp mới nhất trước
    reports.sort((a, b) => b.date.localeCompare(a.date));
    writeFileSync(join(REPORTS_DIR, "index.json"), JSON.stringify(reports, null, 2), "utf-8");
}
function ensureReportsDir() {
    if (!existsSync(REPORTS_DIR))
        mkdirSync(REPORTS_DIR, { recursive: true });
}
function readKnowledgeFile(relativePath) {
    const fullPath = join(KNOWLEDGE_DIR, relativePath);
    if (!existsSync(fullPath)) {
        return `File not found: ${relativePath}\nKnowledge directory: ${KNOWLEDGE_DIR}`;
    }
    return readFileSync(fullPath, "utf-8");
}
function listKnowledgeFiles() {
    const files = [];
    function walk(dir, prefix = "") {
        if (!existsSync(dir))
            return;
        const entries = readdirSync(dir, { withFileTypes: true });
        for (const entry of entries) {
            if (entry.name.startsWith("."))
                continue;
            const rel = prefix ? `${prefix}/${entry.name}` : entry.name;
            if (entry.isDirectory()) {
                walk(join(dir, entry.name), rel);
            }
            else if (entry.name.endsWith(".md")) {
                files.push(rel);
            }
        }
    }
    walk(KNOWLEDGE_DIR);
    return files.join("\n");
}
export function getKnowledgeTools() {
    return [
        {
            name: "buffett_list",
            description: "List all available Warren Buffett investment knowledge files. " +
                "Use this first to discover what knowledge is available before reading specific files.",
            inputSchema: {},
            handler: async () => {
                const files = listKnowledgeFiles();
                return {
                    content: [
                        {
                            type: "text",
                            text: `# Warren Buffett Knowledge Base — Available Files\n\n${files}\n\nUse buffett_read to read any file.`,
                        },
                    ],
                };
            },
        },
        {
            name: "buffett_read",
            description: "Read a specific Warren Buffett investment knowledge file. " +
                "Use this to get detailed knowledge about investment principles, analysis frameworks, " +
                "valuation methods, sector analysis, and decision checklists.\n\n" +
                "Key files:\n" +
                "- README.md → Overview and navigation guide\n" +
                "- 01_philosophy/core_principles.md → Core investment philosophy\n" +
                "- 01_philosophy/mental_models.md → Mental models (compound interest, moat, etc.)\n" +
                "- 02_business_analysis/competitive_advantage.md → Economic moat analysis\n" +
                "- 02_business_analysis/business_quality_checklist.md → Business quality scoring\n" +
                "- 02_business_analysis/management_evaluation.md → How to evaluate management\n" +
                "- 03_financial_analysis/key_metrics.md → Key financial metrics (ROE, FCF, etc.)\n" +
                "- 03_financial_analysis/balance_sheet_analysis.md → Balance sheet analysis\n" +
                "- 03_financial_analysis/earnings_power.md → Earnings power analysis\n" +
                "- 04_valuation/intrinsic_value.md → How to calculate intrinsic value\n" +
                "- 04_valuation/margin_of_safety.md → Margin of safety concept\n" +
                "- 05_portfolio_management/concentration_strategy.md → Portfolio concentration\n" +
                "- 05_portfolio_management/when_to_sell.md → When to sell stocks\n" +
                "- 05_portfolio_management/position_sizing.md → Position sizing\n" +
                "- 06_market_psychology/mr_market.md → Market psychology & cognitive biases\n" +
                "- 07_sector_analysis/preferred_sectors.md → Sectors Buffett loves/avoids\n" +
                "- 07_sector_analysis/financial_sector_analysis.md → Banking sector analysis\n" +
                "- 08_decision_framework/investment_checklist.md → Complete analysis checklist\n" +
                "- 08_decision_framework/red_flags.md → Warning signs to avoid\n" +
                "- 08_decision_framework/ai_analysis_prompt.md → AI analysis prompt templates",
            inputSchema: {
                file: z
                    .string()
                    .describe("Relative path to knowledge file, e.g. '01_philosophy/core_principles.md' or 'README.md'"),
            },
            handler: async (args) => {
                const content = readKnowledgeFile(args.file);
                return {
                    content: [
                        {
                            type: "text",
                            text: content,
                        },
                    ],
                };
            },
        },
        {
            name: "buffett_analyze_stock",
            description: "Get the complete Investment Council analysis framework for analyzing a Vietnamese stock. " +
                "Returns the council debate format where Buffett (chairman) and Munger debate, " +
                "vote, and conclude. Buffett chairs and gives the final verdict. " +
                "After calling this tool, use Fireant tools to gather actual data and run the council session.",
            inputSchema: {
                symbol: z
                    .string()
                    .optional()
                    .describe("Optional stock symbol to customize the council session template"),
            },
            handler: async (args) => {
                const councilFormat = readKnowledgeFile("08_decision_framework/council_debate_format.md");
                const redFlags = readKnowledgeFile("08_decision_framework/red_flags.md");
                const symbolNote = args.symbol
                    ? `\n## 🎯 Cổ Phiếu Phân Tích: ${args.symbol.toUpperCase()}\n\n**Trước khi bắt đầu phiên họp, thu thập dữ liệu:**\n1. fireant_company_profile({ symbol: "${args.symbol}" })\n2. fireant_fundamental({ symbol: "${args.symbol}" })\n3. fireant_financial_data({ symbol: "${args.symbol}" })\n4. fireant_financial_reports({ symbol: "${args.symbol}" })\n5. fireant_holders({ symbol: "${args.symbol}" })\n6. fireant_officers({ symbol: "${args.symbol}" })\n7. fireant_dividends({ symbol: "${args.symbol}" })\n\nSau khi có đủ dữ liệu → Mở phiên họp Hội Đồng theo format bên dưới.\n`
                    : "";
                return {
                    content: [
                        {
                            type: "text",
                            text: `# 🏛️ Investment Council — Phân Tích Framework\n${symbolNote}\n---\n\n${councilFormat}\n\n---\n\n## RED FLAGS CHECKLIST (Buffett × Munger)\n\n${redFlags}`,
                        },
                    ],
                };
            },
        },
        {
            name: "buffett_sector_guide",
            description: "Get Warren Buffett's sector preferences for Vietnamese stock market. " +
                "Returns which sectors to favor (banking, consumer staples, utilities) and which to avoid (airlines, commodities). " +
                "Includes specific guidance for Vietnamese market context.",
            inputSchema: {
                sector: z
                    .string()
                    .optional()
                    .describe("Optional sector name to get specific guidance (e.g. 'banking', 'steel', 'consumer', 'tech')"),
            },
            handler: async (args) => {
                const preferred = readKnowledgeFile("07_sector_analysis/preferred_sectors.md");
                const banking = readKnowledgeFile("07_sector_analysis/financial_sector_analysis.md");
                let result = preferred;
                if (args.sector) {
                    const s = args.sector.toLowerCase();
                    if (s.includes("bank") ||
                        s.includes("ngân hàng") ||
                        s.includes("finance") ||
                        s.includes("tài chính")) {
                        result = `${preferred}\n\n---\n\n## BANKING SECTOR DEEP DIVE\n\n${banking}`;
                    }
                }
                return {
                    content: [
                        {
                            type: "text",
                            text: result,
                        },
                    ],
                };
            },
        },
        {
            name: "buffett_valuation_guide",
            description: "Get Warren Buffett's valuation methodology including intrinsic value calculation, " +
                "DCF approach, margin of safety requirements, and how to apply them to Vietnamese stocks.",
            inputSchema: {},
            handler: async () => {
                const iv = readKnowledgeFile("04_valuation/intrinsic_value.md");
                const mos = readKnowledgeFile("04_valuation/margin_of_safety.md");
                const ep = readKnowledgeFile("03_financial_analysis/earnings_power.md");
                return {
                    content: [
                        {
                            type: "text",
                            text: `# Warren Buffett Valuation Methodology\n\n## PART 1: INTRINSIC VALUE\n\n${iv}\n\n---\n\n## PART 2: MARGIN OF SAFETY\n\n${mos}\n\n---\n\n## PART 3: EARNINGS POWER ANALYSIS\n\n${ep}`,
                        },
                    ],
                };
            },
        },
        // ── SECOND BRAIN TOOLS ─────────────────────────────────────────────────
        {
            name: "buffett_save_report",
            description: "Lưu báo cáo phân tích cổ phiếu vào Second Brain (knowledge/reports/). " +
                "GỌI TOOL NÀY sau khi hoàn thành phân tích đầy đủ để lưu trữ lại. " +
                "Báo cáo được lưu với YAML frontmatter để dễ tìm kiếm sau này.",
            inputSchema: {
                symbol: z.string().describe("Mã cổ phiếu, VD: MBB, VCB, HPG"),
                company: z.string().describe("Tên đầy đủ công ty"),
                content: z.string().describe("Nội dung báo cáo đầy đủ (Markdown — toàn bộ phân tích)"),
                price: z.number().describe("Giá cổ phiếu tại ngày phân tích (VNĐ)"),
                verdict: z
                    .enum(["MUA_MANH", "MUA", "THEO_DOI", "TRANH"])
                    .describe("Phán quyết của Hội Đồng: MUA_MANH/MUA/THEO_DOI/TRANH"),
                score: z.number().min(0).max(56).describe("Điểm Buffett Scorecard (0-56)"),
                sector: z.string().describe("Ngành kinh doanh, VD: banking, steel, retail, realestate"),
                tags: z
                    .array(z.string())
                    .optional()
                    .describe("Tags bổ sung, VD: ['state-owned', 'dividend', 'CASA']"),
                date: z
                    .string()
                    .optional()
                    .describe("Ngày phân tích YYYY-MM-DD, mặc định là ngày hôm nay"),
            },
            handler: async (args) => {
                ensureReportsDir();
                const sym = args.symbol.toUpperCase();
                const date = args.date ?? new Date().toISOString().slice(0, 10);
                const tags = args.tags ?? [];
                // Tạo thư mục cho symbol
                const symDir = join(REPORTS_DIR, sym);
                if (!existsSync(symDir))
                    mkdirSync(symDir, { recursive: true });
                // Tạo nội dung với YAML frontmatter
                const frontmatter = [
                    "---",
                    `symbol: ${sym}`,
                    `company: ${args.company}`,
                    `date: ${date}`,
                    `price: ${args.price}`,
                    `verdict: ${args.verdict}`,
                    `score: ${args.score}`,
                    `sector: ${args.sector}`,
                    `tags: [${tags.join(", ")}]`,
                    "---",
                    "",
                ].join("\n");
                const filePath = join(symDir, `${date}.md`);
                writeFileSync(filePath, frontmatter + args.content, "utf-8");
                // Cập nhật index.json
                const index = loadIndex().filter((r) => !(r.symbol === sym && r.date === date));
                index.push({
                    symbol: sym,
                    company: args.company,
                    date,
                    price: args.price,
                    verdict: args.verdict,
                    score: args.score,
                    sector: args.sector,
                    tags,
                    file: `${sym}/${date}.md`,
                });
                saveIndex(index);
                return {
                    content: [
                        {
                            type: "text",
                            text: `✅ Báo cáo đã lưu vào Second Brain\n\n` +
                                `📁 File: knowledge/reports/${sym}/${date}.md\n` +
                                `📊 ${sym} | ${args.verdict} | Điểm: ${args.score}/56 | Giá: ${args.price.toLocaleString("vi-VN")} VNĐ\n` +
                                `🏷️ Sector: ${args.sector} | Tags: ${tags.join(", ") || "(không có)"}\n\n` +
                                `Dùng buffett_read_report(symbol='${sym}') để đọc lại.`,
                        },
                    ],
                };
            },
        },
        {
            name: "buffett_list_reports",
            description: "Liệt kê tất cả báo cáo đã lưu trong Second Brain. " +
                "Có thể lọc theo symbol, verdict, sector. Trả về bảng tóm tắt với metadata.",
            inputSchema: {
                symbol: z.string().optional().describe("Lọc theo mã cổ phiếu, VD: MBB"),
                verdict: z
                    .enum(["MUA_MANH", "MUA", "THEO_DOI", "TRANH"])
                    .optional()
                    .describe("Lọc theo phán quyết"),
                sector: z.string().optional().describe("Lọc theo ngành, VD: banking"),
                limit: z.number().optional().describe("Số báo cáo tối đa trả về (mặc định 30)"),
            },
            handler: async (args) => {
                let reports = loadIndex();
                if (args.symbol) {
                    const sym = args.symbol.toUpperCase();
                    reports = reports.filter((r) => r.symbol === sym);
                }
                if (args.verdict) {
                    reports = reports.filter((r) => r.verdict === args.verdict);
                }
                if (args.sector) {
                    reports = reports.filter((r) => r.sector.toLowerCase().includes(args.sector.toLowerCase()));
                }
                const limit = args.limit ?? 30;
                reports = reports.slice(0, limit);
                if (reports.length === 0) {
                    return {
                        content: [
                            {
                                type: "text",
                                text: "📭 Chưa có báo cáo nào trong Second Brain phù hợp với bộ lọc.",
                            },
                        ],
                    };
                }
                const verdictEmoji = {
                    MUA_MANH: "🟢",
                    MUA: "🟡",
                    THEO_DOI: "🟠",
                    TRANH: "🔴",
                };
                const rows = reports
                    .map((r) => `| ${verdictEmoji[r.verdict] ?? "⚪"} ${r.symbol} ` +
                    `| ${r.company} ` +
                    `| ${r.date} ` +
                    `| ${r.price.toLocaleString("vi-VN")} VNĐ ` +
                    `| ${r.verdict} ` +
                    `| ${r.score}/56 ` +
                    `| ${r.sector} |`)
                    .join("\n");
                const table = `| Symbol | Công Ty | Ngày | Giá | Verdict | Điểm | Sector |\n` +
                    `|--------|---------|------|-----|---------|------|--------|\n` +
                    rows;
                return {
                    content: [
                        {
                            type: "text",
                            text: `# 🧠 Second Brain — Danh Sách Báo Cáo (${reports.length} báo cáo)\n\n` +
                                table +
                                `\n\nDùng buffett_read_report(symbol='XXX') để đọc chi tiết.`,
                        },
                    ],
                };
            },
        },
        {
            name: "buffett_read_report",
            description: "Đọc một báo cáo phân tích từ Second Brain. " +
                "Nếu không chỉ định ngày, sẽ đọc báo cáo mới nhất của symbol đó.",
            inputSchema: {
                symbol: z.string().describe("Mã cổ phiếu, VD: MBB"),
                date: z
                    .string()
                    .optional()
                    .describe("Ngày báo cáo YYYY-MM-DD. Bỏ trống để đọc báo cáo mới nhất."),
            },
            handler: async (args) => {
                const sym = args.symbol.toUpperCase();
                const symDir = join(REPORTS_DIR, sym);
                if (!existsSync(symDir)) {
                    return {
                        content: [
                            {
                                type: "text",
                                text: `❌ Chưa có báo cáo nào cho ${sym} trong Second Brain.\nDùng buffett_save_report để lưu báo cáo đầu tiên.`,
                            },
                        ],
                    };
                }
                let targetDate = args.date;
                if (!targetDate) {
                    // Tìm báo cáo mới nhất
                    const files = readdirSync(symDir)
                        .filter((f) => f.endsWith(".md"))
                        .sort()
                        .reverse();
                    if (files.length === 0) {
                        return {
                            content: [
                                {
                                    type: "text",
                                    text: `❌ Thư mục ${sym} tồn tại nhưng không có báo cáo nào.`,
                                },
                            ],
                        };
                    }
                    targetDate = files[0].replace(".md", "");
                }
                const filePath = join(symDir, `${targetDate}.md`);
                if (!existsSync(filePath)) {
                    return {
                        content: [
                            {
                                type: "text",
                                text: `❌ Không tìm thấy báo cáo ${sym} ngày ${targetDate}.\nDùng buffett_list_reports(symbol='${sym}') để xem các báo cáo có sẵn.`,
                            },
                        ],
                    };
                }
                const content = readFileSync(filePath, "utf-8");
                return {
                    content: [
                        {
                            type: "text",
                            text: `# 📋 Báo Cáo Second Brain: ${sym} — ${targetDate}\n\n${content}`,
                        },
                    ],
                };
            },
        },
        {
            name: "buffett_search_reports",
            description: "Tìm kiếm báo cáo trong Second Brain theo keyword, verdict, hoặc sector. " +
                "Hữu ích khi muốn tìm tất cả cổ phiếu ngân hàng đã phân tích, hoặc các cổ phiếu có verdict MUA.",
            inputSchema: {
                query: z
                    .string()
                    .optional()
                    .describe("Từ khóa tìm kiếm trong nội dung báo cáo (case-insensitive)"),
                verdict: z
                    .enum(["MUA_MANH", "MUA", "THEO_DOI", "TRANH"])
                    .optional()
                    .describe("Lọc theo phán quyết"),
                sector: z.string().optional().describe("Lọc theo ngành"),
                tag: z.string().optional().describe("Lọc theo tag"),
            },
            handler: async (args) => {
                let reports = loadIndex();
                // Lọc theo metadata
                if (args.verdict) {
                    reports = reports.filter((r) => r.verdict === args.verdict);
                }
                if (args.sector) {
                    reports = reports.filter((r) => r.sector.toLowerCase().includes(args.sector.toLowerCase()));
                }
                if (args.tag) {
                    const t = args.tag.toLowerCase();
                    reports = reports.filter((r) => r.tags.some((tag) => tag.toLowerCase().includes(t)));
                }
                // Tìm kiếm keyword trong nội dung file
                if (args.query) {
                    const q = args.query.toLowerCase();
                    reports = reports.filter((r) => {
                        const filePath = join(REPORTS_DIR, r.file);
                        if (!existsSync(filePath))
                            return false;
                        const content = readFileSync(filePath, "utf-8").toLowerCase();
                        return content.includes(q);
                    });
                }
                if (reports.length === 0) {
                    return {
                        content: [
                            {
                                type: "text",
                                text: "🔍 Không tìm thấy báo cáo nào phù hợp với điều kiện tìm kiếm.",
                            },
                        ],
                    };
                }
                const verdictEmoji = {
                    MUA_MANH: "🟢",
                    MUA: "🟡",
                    THEO_DOI: "🟠",
                    TRANH: "🔴",
                };
                const results = reports
                    .map((r) => `- ${verdictEmoji[r.verdict] ?? "⚪"} **${r.symbol}** (${r.company}) ` +
                    `— ${r.verdict} | ${r.score}/56 | ${r.date} | ${r.price.toLocaleString("vi-VN")} VNĐ`)
                    .join("\n");
                const filters = [
                    args.query ? `keyword: "${args.query}"` : null,
                    args.verdict ? `verdict: ${args.verdict}` : null,
                    args.sector ? `sector: ${args.sector}` : null,
                    args.tag ? `tag: ${args.tag}` : null,
                ]
                    .filter(Boolean)
                    .join(" | ");
                return {
                    content: [
                        {
                            type: "text",
                            text: `# 🔍 Kết Quả Tìm Kiếm Second Brain\n` +
                                `**Bộ lọc:** ${filters || "(tất cả)"}\n` +
                                `**Tìm thấy:** ${reports.length} báo cáo\n\n` +
                                results +
                                `\n\nDùng buffett_read_report(symbol='XXX') để đọc chi tiết.`,
                        },
                    ],
                };
            },
        },
    ];
}
