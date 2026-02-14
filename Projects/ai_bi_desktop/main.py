#!/usr/bin/env python3
"""
AI BI Desktop Application
=========================
Main entry point for the application

Usage:
    python main.py                    # Start background service
    python main.py --dashboard        # Open dashboard directly
    python main.py --analyze data.csv # Analyze file directly
"""

import sys
import argparse
from pathlib import Path



# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from loguru import logger
from config.settings import app_config
from core.background_service import main as run_background_service
from core.orchestrator import quick_analyze
from ui.gradio_app import launch_dashboard


def main():
    """
    Main entry point with CLI argument parsing
    """
    parser = argparse.ArgumentParser(
        description=f'{app_config.app_name} - Intelligent BI & AutoML Desktop Assistant',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                          Start background service
  python main.py --dashboard              Open dashboard directly
  python main.py --analyze data.csv       Analyze a dataset
  python main.py --analyze data.csv --target price  Specify target column
  python main.py --port 8080              Use custom port
        """
    )
    
    parser.add_argument(
        '--dashboard', '-d',
        action='store_true',
        help='Launch dashboard directly without background service'
    )
    
    parser.add_argument(
        '--analyze', '-a',
        type=str,
        metavar='FILE',
        help='Analyze a dataset file directly'
    )
    
    parser.add_argument(
        '--target', '-t',
        type=str,
        metavar='COLUMN',
        help='Target column name (for --analyze)'
    )
    
    parser.add_argument(
        '--port', '-p',
        type=int,
        default=app_config.gradio_port,
        metavar='PORT',
        help=f'Port for Gradio dashboard (default: {app_config.gradio_port})'
    )
    
    parser.add_argument(
        '--share',
        action='store_true',
        help='Create public share link for dashboard'
    )
    
    parser.add_argument(
        '--version', '-v',
        action='version',
        version=f'{app_config.app_name} v{app_config.version}'
    )
    
    args = parser.parse_args()
    
    # Handle different modes
    if args.analyze:
        # Direct analysis mode
        run_direct_analysis(args.analyze, args.target)
    
    elif args.dashboard:
        # Dashboard only mode
        run_dashboard(args.port, args.share)
    
    else:
        # Background service mode (default)
        run_background_service()


def run_direct_analysis(file_path: str, target_col: str = None):
    """
    Run direct analysis on a file
    """
    logger.info("=" * 60)
    logger.info("Running Direct Analysis Mode")
    logger.info("=" * 60)
    
    try:
        file_path = Path(file_path)
        
        if not file_path.exists():
            logger.error(f"File not found: {file_path}")
            sys.exit(1)
        
        logger.info(f"Analyzing: {file_path}")
        if target_col:
            logger.info(f"Target column: {target_col}")
        
        # Run analysis
        result = quick_analyze(str(file_path), target_col)


        # Print results
        print("\n" + "=" * 60)
        print("ANALYSIS COMPLETE")
        print("=" * 60)
        
        print(f"\n📊 Target: {result.selected_target.column_name}")
        print(f"   Task Type: {result.selected_target.task_type}")
        print(f"   Confidence: {result.selected_target.confidence_score:.2%}")
        
        print(f"\n🤖 Best Model: {result.best_model.model_name}")
        print(f"   CV Score: {result.best_model.mean_cv_score:.4f} ± {result.best_model.std_cv_score:.4f}")
        
        print(f"\n🔥 Top 5 Features:")
        for i, corr in enumerate(result.correlations[:5], 1):
            print(f"   {i}. {corr.feature_name} (r={corr.correlation_value:.3f}, {corr.test_type})")
        
        print(f"\n💡 Generated {len(result.insights)} AI insights")
        
        print("\n" + "=" * 60)
        print("To view interactive dashboard, run:")
        print(f"  python main.py --dashboard")
        print("=" * 60 + "\n")
        
    except Exception as e:
        logger.error(f"Analysis failed: {e}", exc_info=True)
        sys.exit(1)


def run_dashboard(port: int = 7860, share: bool = False):
    """
    Run dashboard directly
    """
    logger.info("=" * 60)
    logger.info("Launching Dashboard")
    logger.info("=" * 60)
    
    launch_dashboard(share=share, port=port)


if __name__ == "__main__":
    main()
