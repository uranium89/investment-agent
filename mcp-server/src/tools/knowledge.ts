import { z } from "zod";
import { readFileSync, readdirSync, existsSync } from "fs";
import { join, resolve } from "path";
import type { ToolDefinition } from "./types.js";

// Resolve the knowledge base directory relative to the built JS file
// mcp-server/build/tools/knowledge.js → ../../knowledge (project root/knowledge)
const KNOWLEDGE_DIR = resolve(import.meta.dirname ?? __dirname, "../../../knowledge");

function readKnowledgeFile(relativePath: string): string {
  const fullPath = join(KNOWLEDGE_DIR, relativePath);
  if (!existsSync(fullPath)) {
    return `File not found: ${relativePath}\nAvailable directory: ${KNOWLEDGE_DIR}`;
  }
  return readFileSync(fullPath, "utf-8");
}

function listKnowledgeFiles(): string {
  const files: string[] = [];

  function walk(dir: string, prefix = "") {
    if (!existsSync(dir)) return;
    const entries = readdirSync(dir, { withFileTypes: true });
    for (const entry of entries) {
      if (entry.name.startsWith(".")) continue;
      const rel = prefix ? `${prefix}/${entry.name}` : entry.name;
      if (entry.isDirectory()) {
        walk(join(dir, entry.name), rel);
      } else if (entry.name.endsWith(".md")) {
        files.push(rel);
      }
    }
  }

  walk(KNOWLEDGE_DIR);
  return files.join("\n");
}

export function getKnowledgeTools(): ToolDefinition[] {
  return [
    {
      name: "buffett_knowledge_list",
      description:
        "List all available Warren Buffett investment knowledge files. " +
        "Use this first to discover what knowledge is available before reading specific files.",
      inputSchema: {},
      handler: async () => {
        const files = listKnowledgeFiles();
        return {
          content: [
            {
              type: "text" as const,
              text: `# Warren Buffett Knowledge Base — Available Files\n\n${files}\n\nUse buffett_knowledge_read to read any file.`,
            },
          ],
        };
      },
    },

    {
      name: "buffett_knowledge_read",
      description:
        "Read a specific Warren Buffett investment knowledge file. " +
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
          .describe(
            "Relative path to knowledge file, e.g. '01_philosophy/core_principles.md' or 'README.md'"
          ),
      },
      handler: async (args: { file: string }) => {
        const content = readKnowledgeFile(args.file);
        return {
          content: [
            {
              type: "text" as const,
              text: content,
            },
          ],
        };
      },
    },

    {
      name: "buffett_analyze_stock",
      description:
        "Get the complete Warren Buffett analysis framework and checklist for analyzing a Vietnamese stock. " +
        "Returns the full analysis template, scoring criteria, and step-by-step process to evaluate any stock. " +
        "After calling this tool, use Fireant tools to gather actual data and fill in the analysis.",
      inputSchema: {
        symbol: z
          .string()
          .optional()
          .describe("Optional stock symbol to customize the analysis template"),
      },
      handler: async (args: { symbol?: string }) => {
        const checklist = readKnowledgeFile("08_decision_framework/investment_checklist.md");
        const redFlags = readKnowledgeFile("08_decision_framework/red_flags.md");
        const metrics = readKnowledgeFile("03_financial_analysis/key_metrics.md");

        const symbolNote = args.symbol
          ? `\n## 🎯 Analyzing: ${args.symbol.toUpperCase()}\n\nNext steps:\n1. Call fireant_fundamental({ symbol: "${args.symbol}" })\n2. Call fireant_financial_data({ symbol: "${args.symbol}" })\n3. Call fireant_company_profile({ symbol: "${args.symbol}" })\n4. Call fireant_holders({ symbol: "${args.symbol}" })\n5. Fill in the checklist below with the data\n`
          : "";

        return {
          content: [
            {
              type: "text" as const,
              text: `# Warren Buffett Analysis Framework\n${symbolNote}\n---\n\n## PART 1: KEY METRICS REFERENCE\n\n${metrics}\n\n---\n\n## PART 2: INVESTMENT CHECKLIST\n\n${checklist}\n\n---\n\n## PART 3: RED FLAGS TO CHECK\n\n${redFlags}`,
            },
          ],
        };
      },
    },

    {
      name: "buffett_sector_guide",
      description:
        "Get Warren Buffett's sector preferences for Vietnamese stock market. " +
        "Returns which sectors to favor (banking, consumer staples, utilities) and which to avoid (airlines, commodities). " +
        "Includes specific guidance for Vietnamese market context.",
      inputSchema: {
        sector: z
          .string()
          .optional()
          .describe(
            "Optional sector name to get specific guidance (e.g. 'banking', 'steel', 'consumer', 'tech')"
          ),
      },
      handler: async (args: { sector?: string }) => {
        const preferred = readKnowledgeFile("07_sector_analysis/preferred_sectors.md");
        const banking = readKnowledgeFile("07_sector_analysis/financial_sector_analysis.md");

        let result = preferred;

        if (args.sector) {
          const s = args.sector.toLowerCase();
          if (
            s.includes("bank") ||
            s.includes("ngân hàng") ||
            s.includes("finance") ||
            s.includes("tài chính")
          ) {
            result = `${preferred}\n\n---\n\n## BANKING SECTOR DEEP DIVE\n\n${banking}`;
          }
        }

        return {
          content: [
            {
              type: "text" as const,
              text: result,
            },
          ],
        };
      },
    },

    {
      name: "buffett_valuation_guide",
      description:
        "Get Warren Buffett's valuation methodology including intrinsic value calculation, " +
        "DCF approach, margin of safety requirements, and how to apply them to Vietnamese stocks.",
      inputSchema: {},
      handler: async () => {
        const iv = readKnowledgeFile("04_valuation/intrinsic_value.md");
        const mos = readKnowledgeFile("04_valuation/margin_of_safety.md");
        const ep = readKnowledgeFile("03_financial_analysis/earnings_power.md");

        return {
          content: [
            {
              type: "text" as const,
              text: `# Warren Buffett Valuation Methodology\n\n## PART 1: INTRINSIC VALUE\n\n${iv}\n\n---\n\n## PART 2: MARGIN OF SAFETY\n\n${mos}\n\n---\n\n## PART 3: EARNINGS POWER ANALYSIS\n\n${ep}`,
            },
          ],
        };
      },
    },
  ];
}
