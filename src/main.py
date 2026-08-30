import argparse
import sys
from src.config_loader import load_config
from src.logger import setup_logger

def main():
    parser = argparse.ArgumentParser(description="Mutual Fund FAQ Assistant - RAG Pipeline CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Scrape command
    scrape_parser = subparsers.add_parser("scrape", help="Run the scraper on the 9 fund URLs")
    
    # Ingest command
    ingest_parser = subparsers.add_parser("ingest", help="Run the full ingestion pipeline (scrape -> embed -> store)")

    # Query command
    query_parser = subparsers.add_parser("query", help="Query the RAG pipeline")
    query_parser.add_argument("question", type=str, nargs="?", help="The natural language question to ask")
    query_parser.add_argument("--interactive", action="store_true", help="Enter an interactive REPL loop")



    # Evaluate command
    evaluate_parser = subparsers.add_parser("evaluate", help="Run experiments and evaluate against test questions")

    args = parser.parse_args()

    # Load configuration
    try:
        config = load_config()
    except Exception as e:
        print(f"Failed to load configuration: {e}")
        sys.exit(1)

    # Initialize main logger
    logger = setup_logger("main", config)

    if args.command == "scrape":
        logger.info("Executing 'scrape' command...")
        from src.scraper.scraper import Scraper
        scraper = Scraper(config.get("scraper", {}))
        scraper.scrape_all()
        print("Scraping completed. Raw data saved to configured output directory.")
        
    elif args.command == "ingest":
        logger.info("Executing 'ingest' command...")
        print("Ingest command not fully implemented yet.")
        
    elif args.command == "query":
        logger.info("Executing 'query' command...")
        if args.interactive:
            print("Entering interactive mode. Type 'exit' to quit.")
            while True:
                q = input("Question: ")
                if q.strip().lower() in ["exit", "quit"]:
                    break
                print(f"Answering: {q} (Not implemented)")
        elif args.question:
            print(f"Question: {args.question}")
            print("Answering... (Not implemented)")
        else:
            query_parser.print_help()
            

    elif args.command == "evaluate":
        logger.info("Executing 'evaluate' command...")
        print("Evaluate command not fully implemented yet.")
        
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
