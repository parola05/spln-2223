import argparse
from name_shield import NameShield
from address_shield import AddressShield
from document_shield import DocumentShield

def main():
    parser = argparse.ArgumentParser(
        prog="Shield",
        description="Data anonymizer tool",
        epilog="Build by Henrique, José and Alex"
    )

    parser.add_argument('filename')
    parser.add_argument('-n','--name', action='store_true', help="anonymize only names")
    parser.add_argument('-d','--document', action='store_true', help="anonymize only documents")
    parser.add_argument('-a','--address', action='store_true', help="anonymize only addresses")
    parser.add_argument('-o','--output', help="output file")

    args = parser.parse_args()
    filename = args.filename
    text = ""

    if filename:
        with open(filename,"r") as f:
            text  = f.read() 

        if args.name:
            name = NameShield(text=text)
            print(name.shield())

        if args.document:
            text = DocumentShield(text=text).shield()

        if args.address:
            text = AddressShield(text=text).shield()

        if args.output:
            with open(args.output,"w") as f:
                f.write(text)
        else:
            #print(text)
            pass

if __name__ == "__main__":
    main()