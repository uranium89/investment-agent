import { z } from "zod";
import { readFileSync, readdirSync, existsSync } from "fs";
import { join, resolve } from "path";
// Resolve the Industry knowledge base directory.
// Priority: INDUSTRY_KNOWLEDGE_DIR env var → relative path from built JS file
// (mcp-server-industry/build/tools/knowledge.js → ../../../knowledge/industries)
const INDUSTRY_DIR = process.env.INDUSTRY_KNOWLEDGE_DIR
    ? resolve(process.env.INDUSTRY_KNOWLEDGE_DIR)
    : resolve(import.meta.dirname ?? __dirname, "../../../knowledge/industries");
// ─── Helpers ────────────────────────────────────────────────────────────────
function readFile(relativePath) {
    const fullPath = join(INDUSTRY_DIR, relativePath);
    if (!existsSync(fullPath)) {
        return `File not found: ${relativePath}\nIndustry knowledge directory: ${INDUSTRY_DIR}`;
    }
    return readFileSync(fullPath, "utf-8");
}
function listSectors() {
    if (!existsSync(INDUSTRY_DIR))
        return [];
    return readdirSync(INDUSTRY_DIR, { withFileTypes: true })
        .filter((e) => e.isDirectory())
        .map((e) => e.name);
}
function listFilesInSector(sector) {
    const sectorDir = join(INDUSTRY_DIR, sector);
    if (!existsSync(sectorDir))
        return [];
    return readdirSync(sectorDir)
        .filter((f) => f.endsWith(".md"))
        .map((f) => f.replace(".md", ""));
}
function searchInSector(sector, query) {
    const sectorDir = join(INDUSTRY_DIR, sector);
    if (!existsSync(sectorDir))
        return [];
    const results = [];
    const q = query.toLowerCase();
    const files = readdirSync(sectorDir).filter((f) => f.endsWith(".md"));
    for (const file of files) {
        const content = readFileSync(join(sectorDir, file), "utf-8");
        if (content.toLowerCase().includes(q)) {
            // Extract context around the match
            const idx = content.toLowerCase().indexOf(q);
            const start = Math.max(0, idx - 100);
            const end = Math.min(content.length, idx + 200);
            const excerpt = content.slice(start, end).replace(/\n/g, " ").trim();
            results.push({ file: file.replace(".md", ""), excerpt: `...${excerpt}...` });
        }
    }
    return results;
}
// ─── SECTOR DISPLAY NAMES ───────────────────────────────────────────────────
const SECTOR_META = {
    dairy: {
        name: "Ngành Sữa (Dairy)",
        stocks: "VNM, IDP, QNS, MCM",
        emoji: "🥛",
    },
    banking: {
        name: "Ngân Hàng (Banking)",
        stocks: "VCB, BID, CTG, MBB, ACB, TCB",
        emoji: "🏦",
    },
    steel: {
        name: "Thép (Steel)",
        stocks: "HPG, NKG, HSG, TLH",
        emoji: "🔩",
    },
    retail: {
        name: "Bán Lẻ (Retail)",
        stocks: "MWG, FRT, DGW, PNJ",
        emoji: "🛒",
    },
    real_estate: {
        name: "Bất Động Sản (Real Estate)",
        stocks: "VHM, NVL, PDR, KDH",
        emoji: "🏠",
    },
    power: {
        name: "Điện (Power/Energy)",
        stocks: "POW, PC1, REE, GEG",
        emoji: "⚡",
    },
};
const FILE_DESCRIPTIONS = {
    overview: "Tổng quan ngành — quy mô, phân khúc, xu hướng, vị trí trong chuỗi toàn cầu",
    production_process: "Chuỗi giá trị & quy trình kỹ thuật — công nghệ sản xuất, chế biến, chuỗi cung ứng",
    economics: "Unit economics & cơ cấu chi phí — margin benchmark, CAPEX cycle, phân tích tính thời vụ",
    competitive_landscape: "Cấu trúc ngành — Porter's 5 Forces, rào cản gia nhập, động lực cạnh tranh",
    regulatory: "Quy định pháp lý & tiêu chuẩn — TCVN, Codex, HACCP, quy định nhập khẩu, nhãn mác",
};
// ─── TOOLS ──────────────────────────────────────────────────────────────────
export function getIndustryTools() {
    return [
        {
            name: "industry_list",
            description: "Liệt kê tất cả ngành trong Industry Knowledge Base và các files có sẵn trong mỗi ngành. " +
                "Dùng tool này TRƯỚC khi phân tích cổ phiếu để biết kiến thức ngành nào đang có. " +
                "Ví dụ: Trước khi phân tích VNM, gọi industry_list() để thấy có 'dairy/' với 5 files.",
            inputSchema: {
                sector: z
                    .string()
                    .optional()
                    .describe("Tên ngành cụ thể để xem chi tiết files (VD: 'dairy', 'banking'). Bỏ trống để xem tất cả."),
            },
            handler: async (args) => {
                const sectors = listSectors();
                if (sectors.length === 0) {
                    return {
                        content: [
                            {
                                type: "text",
                                text: `❌ Không tìm thấy ngành nào trong ${INDUSTRY_DIR}\nVui lòng kiểm tra cấu hình INDUSTRY_KNOWLEDGE_DIR.`,
                            },
                        ],
                    };
                }
                if (args.sector) {
                    const s = args.sector.toLowerCase();
                    if (!sectors.includes(s)) {
                        return {
                            content: [
                                {
                                    type: "text",
                                    text: `❌ Ngành '${s}' chưa có trong knowledge base.\nCác ngành hiện có: ${sectors.join(", ")}`,
                                },
                            ],
                        };
                    }
                    const files = listFilesInSector(s);
                    const meta = SECTOR_META[s];
                    const fileList = files
                        .map((f) => {
                        const desc = FILE_DESCRIPTIONS[f] ?? "Tài liệu ngành";
                        return `  📄 ${f}.md — ${desc}`;
                    })
                        .join("\n");
                    return {
                        content: [
                            {
                                type: "text",
                                text: `# ${meta?.emoji ?? "🏭"} ${meta?.name ?? s} — Files Có Sẵn\n\n` +
                                    `**Cổ phiếu liên quan:** ${meta?.stocks ?? "N/A"}\n\n` +
                                    `**Files:**\n${fileList}\n\n` +
                                    `**Cách đọc:** \`industry_read(sector='${s}', file='overview')\``,
                            },
                        ],
                    };
                }
                // List all sectors
                const sectorList = sectors
                    .map((s) => {
                    const meta = SECTOR_META[s];
                    const files = listFilesInSector(s);
                    return (`### ${meta?.emoji ?? "🏭"} ${meta?.name ?? s}\n` +
                        `**Cổ phiếu:** ${meta?.stocks ?? "N/A"}\n` +
                        `**Files:** ${files.join(", ")}\n` +
                        `→ \`industry_overview(sector='${s}')\` hoặc \`industry_list(sector='${s}')\``);
                })
                    .join("\n\n");
                return {
                    content: [
                        {
                            type: "text",
                            text: `# 🏭 Industry Knowledge Base — Danh Sách Ngành\n\n` +
                                `**Tổng số ngành:** ${sectors.length}\n\n` +
                                `---\n\n${sectorList}\n\n---\n\n` +
                                `**Tip:** Gọi \`industry_overview(sector='dairy')\` để đọc nhanh tổng quan ngành.`,
                        },
                    ],
                };
            },
        },
        {
            name: "industry_read",
            description: "Đọc một file kiến thức ngành cụ thể. Dùng khi cần thông tin chi tiết về một khía cạnh của ngành. " +
                "Ví dụ: Đọc production_process của dairy để hiểu UHT vs Pasteurization trước khi phân tích VNM.\n\n" +
                "Files thường có trong mỗi ngành:\n" +
                "- overview.md → Tổng quan, quy mô, phân khúc, xu hướng\n" +
                "- production_process.md → Chuỗi giá trị, kỹ thuật sản xuất\n" +
                "- economics.md → Unit economics, margin benchmark, CAPEX\n" +
                "- competitive_landscape.md → Porter's 5 Forces, cấu trúc cạnh tranh\n" +
                "- regulatory.md → Quy định pháp lý, tiêu chuẩn TCVN/quốc tế",
            inputSchema: {
                sector: z
                    .string()
                    .describe("Tên ngành, VD: 'dairy', 'banking', 'steel', 'retail', 'real_estate', 'power'"),
                file: z
                    .string()
                    .describe("Tên file (không cần .md), VD: 'overview', 'production_process', 'economics', 'competitive_landscape', 'regulatory'"),
            },
            handler: async (args) => {
                const sector = args.sector.toLowerCase();
                const fileName = args.file.endsWith(".md") ? args.file : `${args.file}.md`;
                const content = readFile(join(sector, fileName));
                const meta = SECTOR_META[sector];
                return {
                    content: [
                        {
                            type: "text",
                            text: `# ${meta?.emoji ?? "🏭"} ${meta?.name ?? sector} — ${args.file}\n\n` + content,
                        },
                    ],
                };
            },
        },
        {
            name: "industry_overview",
            description: "Đọc nhanh tổng quan một ngành — kết hợp overview + economics thành 1 lần gọi. " +
                "Dùng ở BẮT ĐẦU phân tích cổ phiếu để nắm bức tranh ngành trước khi đi vào chi tiết. " +
                "VD: Trước khi phân tích VNM → industry_overview(sector='dairy') để hiểu quy mô, phân khúc, benchmark margin.",
            inputSchema: {
                sector: z
                    .string()
                    .describe("Tên ngành: 'dairy', 'banking', 'steel', 'retail', 'real_estate', 'power'"),
            },
            handler: async (args) => {
                const sector = args.sector.toLowerCase();
                const meta = SECTOR_META[sector];
                const overview = readFile(join(sector, "overview.md"));
                const economics = readFile(join(sector, "economics.md"));
                const availableFiles = listFilesInSector(sector);
                const moreFiles = availableFiles
                    .filter((f) => f !== "overview" && f !== "economics")
                    .map((f) => `\`industry_read(sector='${sector}', file='${f}')\``)
                    .join(" | ");
                return {
                    content: [
                        {
                            type: "text",
                            text: `# ${meta?.emoji ?? "🏭"} ${meta?.name ?? sector} — Industry Overview\n\n` +
                                `> **Cổ phiếu liên quan:** ${meta?.stocks ?? "N/A"}\n\n` +
                                `---\n\n## PHẦN 1: TỔNG QUAN NGÀNH\n\n${overview}\n\n` +
                                `---\n\n## PHẦN 2: KINH TẾ HỌC NGÀNH\n\n${economics}\n\n` +
                                `---\n\n**Đọc thêm chi tiết:** ${moreFiles}`,
                        },
                    ],
                };
            },
        },
        {
            name: "industry_search",
            description: "Tìm kiếm full-text trong toàn bộ Industry Knowledge Base. " +
                "Dùng khi cần tìm thông tin cụ thể (VD: 'UHT margin', 'cold chain cost', 'Tetra Pak', 'HACCP'). " +
                "Trả về tên file và đoạn văn bản liên quan.",
            inputSchema: {
                query: z.string().describe("Từ khóa tìm kiếm (tiếng Việt hoặc Anh đều được)"),
                sector: z
                    .string()
                    .optional()
                    .describe("Giới hạn tìm kiếm trong một ngành cụ thể. Bỏ trống để tìm toàn bộ knowledge base."),
            },
            handler: async (args) => {
                const sectors = args.sector ? [args.sector.toLowerCase()] : listSectors();
                const allResults = [];
                for (const s of sectors) {
                    const results = searchInSector(s, args.query);
                    for (const r of results) {
                        allResults.push({ sector: s, ...r });
                    }
                }
                if (allResults.length === 0) {
                    return {
                        content: [
                            {
                                type: "text",
                                text: `🔍 Không tìm thấy kết quả cho "${args.query}"${args.sector ? ` trong ngành ${args.sector}` : ""}.\n\nThử tìm với từ khóa khác hoặc dùng industry_list() để xem các files có sẵn.`,
                            },
                        ],
                    };
                }
                const resultText = allResults
                    .map((r) => {
                    const meta = SECTOR_META[r.sector];
                    return (`### ${meta?.emoji ?? "🏭"} ${r.sector}/${r.file}.md\n` +
                        `> ${r.excerpt}\n` +
                        `→ Đọc đầy đủ: \`industry_read(sector='${r.sector}', file='${r.file}')\``);
                })
                    .join("\n\n");
                return {
                    content: [
                        {
                            type: "text",
                            text: `# 🔍 Kết Quả Tìm Kiếm: "${args.query}"\n\n` +
                                `**Tìm thấy:** ${allResults.length} file liên quan\n\n---\n\n${resultText}`,
                        },
                    ],
                };
            },
        },
    ];
}
