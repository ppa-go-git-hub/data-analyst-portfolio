from argparse import ArgumentParser
import logging
import pandas as pd
import sklearn
import joblib

RESET_ASCII = "\x1b[0m"
BOLD_ASCII = "\x1b[1m"
LEVELNO_COLOR_ASCII = {
    logging.NOTSET  : "\x1b[36m", # Cyan
    logging.DEBUG   : "\x1b[34m", # Blue
    logging.INFO    : "\x1b[32m", # Green
    logging.WARNING : "\x1b[33m", # Yellow
    logging.ERROR   : "\x1b[31m", # Red
    logging.CRITICAL: "\x1b[35m", # Magenta
}

class AsciiFormatter(logging.Formatter):
    def format(self, record):
        record.levelname = f"{BOLD_ASCII}{LEVELNO_COLOR_ASCII.get(record.levelno, '')}{record.levelname}{RESET_ASCII}"
        return super().format(record)

def subcommand_csv(model_dump_filename, input_filename, output_filename, drop_features=False):
    logging.info("loading model: start")
    model = joblib.load(model_dump_filename)
    logging.info("loading model: end")
    
    logging.info("reading input: start")
    df = pd.read_csv(input_filename, index_col="id")
    logging.info("reading input: end")
    
    logging.info("running model: start")
    df["is_genuine"] = ~model.predict(df)
    logging.info("running model: end")
    
    logging.info("writing output: start")
    if drop_features:
        df = df[["is_genuine"]]
    df.to_csv(output_filename)
    logging.info("writing output: end")

def subcommand_single(model_dump_filename, *, diagonal, height_left, height_right, margin_low, margin_up, length):
    columns = ("diagonal", "height_left", "height_right", "margin_low", "margin_up", "length")
    record  = ( diagonal ,  height_left ,  height_right ,  margin_low ,  margin_up ,  length )
    df = pd.DataFrame([ record ], columns=columns)
    
    missing_features = df.columns[ df.iloc[0].isna() ]
    if len(missing_features) > 0:
        prefix = f"{len(missing_features)} missing feature{'s' * int(len(missing_features) != 1)}: "
        logging.warning(prefix + ", ".join(missing_features))
    else:
        logging.info("no missing features")
    
    logging.info("loading model: start")
    model = joblib.load(model_dump_filename)
    logging.info("loading model: end")
    
    logging.info("running model: start")
    is_genuine = (~model.predict(df))[0]
    logging.info("running model: end")
    
    print("genuine" if is_genuine else "fake")

def main():
    main_parser = ArgumentParser(description="Automatic detection of non-genuine banknotes")
    verbosity = main_parser.add_mutually_exclusive_group()
    verbosity.set_defaults(logging_level=logging.WARNING)
    verbosity.add_argument("-q", "--quiet"  , action="store_const", dest="logging_level", const=logging.ERROR, help="hide warnings")
    verbosity.add_argument("-v", "--verbose", action="store_const", dest="logging_level", const=logging.INFO , help="show info"    )
    subparsers = main_parser.add_subparsers(dest="subcommand", help="subcommand", required=True)
    
    csv_parser = subparsers.add_parser("csv", description="Prediction for one or many banknotes via CSV files")
    csv_parser.add_argument("-d", "--drop-features", action="store_true", help="drop features from output (kept by default)")
    filenames = csv_parser.add_argument_group("filenames")
    filenames.add_argument("-m", "--model" , metavar="PATH/TO/FILE.joblib", required=True)
    filenames.add_argument("-i", "--input" , metavar="PATH/TO/FILE.csv", required=True)
    filenames.add_argument("-o", "--output", metavar="PATH/TO/FILE.csv", required=True)
    
    single_parser = subparsers.add_parser("single", description="Prediction for one banknote: read features from command line arguments, write prediction to stdout")
    filenames = single_parser.add_argument_group("filenames")
    filenames.add_argument("-m", "--model" , metavar="PATH/TO/FILE.joblib", required=True)
    features = single_parser.add_argument_group("features")
    features.add_argument("--diagonal"    , metavar="VALUE", type=float)
    features.add_argument("--height-left" , metavar="VALUE", type=float)
    features.add_argument("--height-right", metavar="VALUE", type=float)
    features.add_argument("--margin-low"  , metavar="VALUE", type=float)
    features.add_argument("--margin-up"   , metavar="VALUE", type=float)
    features.add_argument("--length"      , metavar="VALUE", type=float)
    
    args = main_parser.parse_args()
    
    logging.basicConfig(level=args.logging_level)
    formatter = AsciiFormatter("[%(levelname)s] %(message)s")
    for handler in logging.getLogger().handlers:
        handler.setFormatter(formatter)
    
    sklearn.set_config(transform_output="pandas")
    
    match args.subcommand:
        case "csv":
            subcommand_csv(args.model, args.input, args.output, args.drop_features)
        case "single":
            subcommand_single(
                args.model,
                diagonal     = args.diagonal,
                height_left  = args.height_left,
                height_right = args.height_right,
                margin_low   = args.margin_low,
                margin_up    = args.margin_up,
                length       = args.length,
            )

if __name__ == "__main__":
    main()