import { z } from "zod";
import { readFileSync, readdirSync, existsSync } from "fs";
import { join, resolve } from "path";
// Resolve the Munger knowledge base directory.
// Priority: MUNGER_KNOWLEDGE_DIR env var → relative path from built JS file
// (mcp-server-munger/build/tools/knowledge.js → ../../../knowledge/munger)
const KNOWLEDGE_DIR = process.env.MUNGER_KNOWLEDGE_DIR
    ? resolve(process.env.MUNGER_KNOWLEDGE_DIR)
    : resolve(import.meta.dirname ?? __dirname, "../../../knowledge/munger");
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
            name: "munger_list",
            description: "List all available Charlie Munger investment knowledge files. " +
                "Use this first to discover what knowledge is available before reading specific files.",
            inputSchema: {},
            handler: async () => {
                const files = listKnowledgeFiles();
                return {
                    content: [
                        {
                            type: "text",
                            text: `# Charlie Munger Knowledge Base — Available Files\n\n${files}\n\nUse munger_read to read any file.`,
                        },
                    ],
                };
            },
        },
        {
            name: "munger_read",
            description: "Read a specific Charlie Munger investment knowledge file. " +
                "Use this to get detailed knowledge about mental models, multidisciplinary thinking, " +
                "inversion, cognitive biases, and decision frameworks.\n\n" +
                "Key files:\n" +
                "- README.md → Overview and navigation guide\n" +
                "- 01_philosophy/core_principles.md → Multidisciplinary thinking, Inversion, Latticework\n" +
                "- 01_philosophy/mental_models_overview.md → Overview of 100+ mental models\n" +
                "- 01_philosophy/latticework_of_models.md → How to combine models for decisions\n" +
                "- 02_mental_models/psychology_models.md → 25 cognitive biases with investment applications\n" +
                "- 02_mental_models/physics_models.md → Inversion, Critical mass, Entropy\n" +
                "- 02_mental_models/economics_models.md → Incentives, Opportunity cost\n" +
                "- 02_mental_models/math_models.md → Compound interest, Probability, Decision trees\n" +
                "- 02_mental_models/biology_models.md → Evolution, Ecosystems, Natural selection\n" +
                "- 03_investing_principles/quality_over_price.md → Wonderful company at fair price\n" +
                "- 03_investing_principles/circle_of_competence.md → Know your limits (Too Hard Pile)\n" +
                "- 03_investing_principles/inversion_in_investing.md → Invert, always invert\n" +
                "- 04_decision_making/munger_checklist.md → Complete investment checklist\n" +
                "- 04_decision_making/avoid_mistakes.md → Lollapalooza effect & bias combinations\n" +
                "- 05_quotes_wisdom/poor_charlies_almanack.md → Lessons from Poor Charlie's Almanack\n" +
                "- 05_quotes_wisdom/famous_speeches.md → USC, Harvard, Wesco, Berkshire speeches",
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
            name: "munger_analyze_stock",
            description: "Get the complete Charlie Munger analysis framework for analyzing a Vietnamese stock. " +
                "Applies multidisciplinary thinking, inversion, mental models, and cognitive bias checks. " +
                "Complements Buffett analysis with deeper focus on qualitative factors and mistake avoidance.",
            inputSchema: {
                symbol: z
                    .string()
                    .optional()
                    .describe("Optional stock symbol to customize the analysis template"),
            },
            handler: async (args) => {
                const checklist = readKnowledgeFile("04_decision_making/munger_checklist.md");
                const avoidMistakes = readKnowledgeFile("04_decision_making/avoid_mistakes.md");
                const inversion = readKnowledgeFile("03_investing_principles/inversion_in_investing.md");
                const symbolNote = args.symbol
                    ? `\n## 🎯 Analyzing: ${args.symbol.toUpperCase()} (Munger Framework)\n\nMunger Analysis Steps:\n1. Circle of Competence check — do I really understand this business?\n2. Inversion — what would kill this investment?\n3. Incentive check — are management incentives aligned?\n4. Bias check — am I being influenced by cognitive biases?\n5. Quality test — is this a "wonderful company"?\n6. Lollapalooza check — are multiple factors pointing the same direction?\n`
                    : "";
                return {
                    content: [
                        {
                            type: "text",
                            text: `# Charlie Munger Analysis Framework\n${symbolNote}\n---\n\n## PART 1: INVERSION — WHAT COULD GO WRONG?\n\n${inversion}\n\n---\n\n## PART 2: INVESTMENT CHECKLIST\n\n${checklist}\n\n---\n\n## PART 3: AVOID THESE MISTAKES\n\n${avoidMistakes}`,
                        },
                    ],
                };
            },
        },
        {
            name: "munger_mental_models",
            description: "Get Charlie Munger's mental models for a specific discipline. " +
                "Returns the key models from that field and how to apply them to investment decisions.",
            inputSchema: {
                discipline: z
                    .enum(["psychology", "physics", "economics", "math", "biology", "all"])
                    .describe("Which discipline's mental models to retrieve. Use 'all' for overview."),
            },
            handler: async (args) => {
                if (args.discipline === "all") {
                    const overview = readKnowledgeFile("01_philosophy/mental_models_overview.md");
                    return {
                        content: [{ type: "text", text: overview }],
                    };
                }
                const fileMap = {
                    psychology: "02_mental_models/psychology_models.md",
                    physics: "02_mental_models/physics_models.md",
                    economics: "02_mental_models/economics_models.md",
                    math: "02_mental_models/math_models.md",
                    biology: "02_mental_models/biology_models.md",
                };
                const file = fileMap[args.discipline];
                if (!file) {
                    return {
                        content: [{ type: "text", text: `Unknown discipline: ${args.discipline}` }],
                    };
                }
                const content = readKnowledgeFile(file);
                return {
                    content: [{ type: "text", text: content }],
                };
            },
        },
        {
            name: "munger_checklist",
            description: "Get Charlie Munger's complete investment checklist and mistake-avoidance framework. " +
                "Includes cognitive bias check, incentive analysis, inversion test, and Lollapalooza check.",
            inputSchema: {},
            handler: async () => {
                const checklist = readKnowledgeFile("04_decision_making/munger_checklist.md");
                const mistakes = readKnowledgeFile("04_decision_making/avoid_mistakes.md");
                return {
                    content: [
                        {
                            type: "text",
                            text: `# Charlie Munger Decision Framework\n\n## PART 1: INVESTMENT CHECKLIST\n\n${checklist}\n\n---\n\n## PART 2: MISTAKES TO AVOID\n\n${mistakes}`,
                        },
                    ],
                };
            },
        },
    ];
}
