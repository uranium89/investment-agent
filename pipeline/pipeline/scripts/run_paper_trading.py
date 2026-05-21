import argparse
import asyncio
import logging
import json
from decimal import Decimal

from pipeline.config import settings
from pipeline.db.connection import async_session_factory
from pipeline.portfolio.paper_trading import run_backtest, run_parameter_sensitivity

logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("paper_trading")


async def main():
    parser = argparse.ArgumentParser(description="VN30 Paper Trading Backtest")
    parser.add_argument("--start", default="2025-06-01", help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end", default="2026-05-21", help="End date (YYYY-MM-DD)")
    parser.add_argument("--capital", type=float, default=100_000_000, help="Initial capital")
    parser.add_argument("--enter", type=float, default=5.0, help="ENTER threshold")
    parser.add_argument("--exit", type=float, default=3.5, help="EXIT threshold")
    parser.add_argument("--max-pos", type=int, default=10, help="Max positions")
    parser.add_argument("--cash", type=float, default=25.0, help="Cash %")
    parser.add_argument("--sensitivity", action="store_true", help="Run parameter sensitivity")
    parser.add_argument("--output", default=None, help="Output JSON file")
    args = parser.parse_args()

    async with async_session_factory() as session:
        if args.sensitivity:
            logger.info("Running parameter sensitivity analysis...")
            results = await run_parameter_sensitivity(
                session, args.start, args.end, Decimal(str(args.capital)),
            )
            print("\n" + "=" * 90)
            print(f"{'Params':40s} {'Return%':8s} {'Sharpe':8s} {'MaxDD%':8s} {'WinRate%':8s} {'Trades':6s}")
            print("-" * 90)
            for r in results:
                print(f"{r['params']:40s} {r['return_pct']:7.1f}% {r['sharpe']:7.3f} {r['max_dd']:7.1f}% {r['win_rate']:7.1f}% {r['trades']:5d}")
            print("=" * 90)

            if args.output:
                with open(args.output, "w") as f:
                    json.dump(results, f, indent=2)
                logger.info("Results saved to %s", args.output)
        else:
            logger.info("Running backtest: %s to %s", args.start, args.end)
            result = await run_backtest(
                session, args.start, args.end,
                initial_capital=Decimal(str(args.capital)),
                enter_threshold=Decimal(str(args.enter)),
                exit_threshold=Decimal(str(args.exit)),
                max_positions=args.max_pos,
                cash_pct=Decimal(str(args.cash)),
            )

            print("\n" + "=" * 50)
            print("BACKTEST RESULTS")
            print("=" * 50)
            print(f"Period:        {args.start} → {args.end}")
            print(f"Initial:       {args.capital:>12,.0f} VND")
            print(f"Final:         {result['final_value']:>12,.0f} VND")
            print(f"Return:        {result['total_return_pct']:>11.2f}%")
            print(f"Annualized:    {result.get('annualized_return_pct', 0):>11.2f}%")
            print(f"Sharpe:        {result.get('sharpe_ratio', 0):>11.3f}")
            print(f"Sortino:       {result.get('sortino_ratio', 0):>11.3f}")
            print(f"Max DD:        {result.get('max_drawdown_pct', 0):>11.2f}%")
            print(f"Calmar:        {result.get('calmar_ratio', 0):>11.3f}")
            print(f"Trades:        {result.get('total_trades', 0):>11}")
            print(f"Win Rate:      {result.get('win_rate_pct', 0):>11.1f}%")
            print(f"Profit Factor: {result.get('profit_factor', 0):>11.2f}")
            print(f"Avg Hold:      {result.get('avg_hold_days', 0):>11.1f} days")
            print(f"Trading Days:  {result.get('trading_days', 0):>11}")
            print(f"Final Pos:     {result['final_positions']:>11}")
            print("=" * 50)

            if args.output:
                with open(args.output, "w") as f:
                    json.dump(result, f, indent=2, default=str)
                logger.info("Results saved to %s", args.output)


if __name__ == "__main__":
    asyncio.run(main())
