import os
import subprocess
from typing import Dict

from pipeline_job import PipelineJob


class DownloadWikiDump(PipelineJob):
    """
    Download the current Wikipedia dump. Either download one file for a dummy / prototyping version
    (set download_data_only_dummy to True). Or all download files.
    """

    def __init__(self, preprocess_jobs: Dict[str, PipelineJob], opts):
        super().__init__(
            requires=[],
            provides=[f"data/versions/{opts.data_version_name}/downloads/{opts.wiki_lang_version}/"],
            preprocess_jobs=preprocess_jobs,
            opts=opts,
        )

    def _run(self):
        self.log("Download finished")
        filename = input("Enter full path: ")
        print("Filename: ", filename)
        file_name = filename.split("/")[-1]

        final_directory = f"data/versions/{self.opts.data_version_name}/downloads/{self.opts.wiki_lang_version}/"
        if not os.path.exists(final_directory):
            os.makedirs(final_directory)
        os.rename(filename, final_directory + file_name)

        return
        self.log(f"Downloading {self.opts.wiki_lang_version}")
        if self.opts.download_data_only_dummy:
            if self.opts.download_2017_enwiki:
                url = "https://archive.org/download/enwiki-20171001/"
                accept = "enwiki-20171001-pages-articles1.xml-p10p30302.bz2"
            else:
                url = f"https://dumps.wikimedia.org/{self.opts.wiki_lang_version}/latest/"
                accept = f"{self.opts.wiki_lang_version}-latest-pages-articles1.xml-*.bz2",
            order = [
                    "wget",
                    "-r",
                    "-l2",
                    "-np",
                    "-nd",
                    url,
                    "-A",
                    accept,
                    "-P",
                    f"data/versions/{self.opts.data_version_name}/downloads/tmp/",
                    # f"data/versions/{self.opts.data_version_name}/downloads/{self.opts.wiki_lang_version}/",
                ]
            print(" ".join(order))
            
            subprocess.check_call(order)
        else:
            if self.opts.download_2017_enwiki:
                url = "https://archive.org/download/enwiki-20171001/"
            else:
                url = f"https://dumps.wikimedia.org/{self.opts.wiki_lang_version}/latest/"
            cmd = [
                    "wget",
                    "-r",
                    "-l2",
                    "-np",
                    "-nd",
                    url,
                    "-A",
                    f"{self.opts.wiki_lang_version}-latest-pages-articles*.xml-*.bz2",
                    "-R",
                    f"{self.opts.wiki_lang_version}-latest-pages-articles-multistream*.xml-*.bz2",
                    "-P",
                    f"data/versions/{self.opts.data_version_name}/downloads/tmp/",
                ]
            cmd = ["wget",
                    "https://archive.org/download/enwiki-20171001/enwiki-20171001-pages-articles.xml.bz2",
                     "-P",
                    "data/versions/dummy/downloads/tmp/",
                    ]

            print(" ".join(cmd))
            subprocess.check_call(cmd)
        os.rename(
            f"data/versions/{self.opts.data_version_name}/downloads/tmp/",
            f"data/versions/{self.opts.data_version_name}/downloads/{self.opts.wiki_lang_version}/",
        )

        self.log("Download finished ")
