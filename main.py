from argparse import ArgumentParser
from pathlib import Path
from shutil import copyfile
from threading import Thread
import logging
from concurrent.futures import ThreadPoolExecutor

'''
--source [-s] picture
--output [-o] 
'''

parser = ArgumentParser(description='Sorting folder')
parser.add_argument("--source", "-s", help="Source folder", required=True)
parser.add_argument("--output", "-o", help="Output folder", default="dist")

args = vars(parser.parse_args())

source = args.get("source")
output = args.get("output")

folders = []
threads_list = []


def grabs_folder(path: Path) -> None:
    for el in path.iterdir():
        if el.is_dir():
            folders.append(el)
            th = Thread(target=grabs_folder, args=(el,))
            threads_list.append(th)
            th.start()


def copy_file(path: Path) -> None:
    for el in path.iterdir():
        if el.is_file():
            ext = el.suffix
            new_path = output_folder / ext
            try:
                new_path.mkdir(exist_ok=True, parents=True)
                copyfile(el, new_path / el.name)
            except OSError as err:
                logging.error(err)


if __name__ == '__main__':
    logging.basicConfig(level=logging.ERROR, format="%(threadName)s %(message)s")
    base_folder = Path(source)
    output_folder = Path(output)
    folders.append(base_folder)

    main_thread = Thread(target=grabs_folder, args=(base_folder,))
    main_thread.start()
    main_thread.join()

    with ThreadPoolExecutor(max_workers=30) as executor:
        results = list(executor.map(copy_file, folders))

    print(f'Were working {len(threads_list)} parse_threads and {len(results)} copy_threads')
    print("Можна видаляти стару папку, якщо треба")
