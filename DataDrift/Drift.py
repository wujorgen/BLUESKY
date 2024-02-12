"""Defines the Drift class."""
import os
import sys

import yaml

from DataDrift.scrapers import gen_carscom_urls, process_carscom, scrape_carscom

from .DriftCar import DriftCar


class Drift:
    """This class houses the guts and data of the scraping system."""

    def __init__(self, path_in: str | bool = False, dict_in=None):
        """
        Initializes the Drift class.

        Args:
            path_in: Path to input yaml. If not given, defaults to current directory.
            dict_in: Dict of inputs. Optional, overrides path_in.
                Format is {"car": ["model1", "model2"]}
        """
        self.ROOTFOLDER = os.getcwd()
        self.OUTPUTFOLDER = os.path.join(self.ROOTFOLDER, "DataDriftOutput")
        if not os.path.isdir(self.OUTPUTFOLDER):
            os.mkdir(self.OUTPUTFOLDER)
        if not path_in:
            self.INPUTFILE = os.path.join(self.ROOTFOLDER, "DataDrift.yaml")
        else:
            self.INPUTFILE = path_in
        if dict_in is None:
            if os.path.exists(self.INPUTFILE):
                with open(self.INPUTFILE, "r") as input_doc:
                    try:
                        self.cardict = yaml.safe_load(input_doc)
                    except yaml.YAMLError:
                        print("ERROR IN INPUT FILE.")
                        sys.exit(-1)
            else:
                print("Oops there's no input file.")
                sys.exit(-404)
        else:
            self.cardict = dict_in

        self.data_carscom = self.scrape_carscom(self.cardict)
        for car in self.data_carscom.keys():
            self.data_carscom[car].writeall(self.OUTPUTFOLDER)

    def scrape_carscom(self, car_dict: dict) -> dict:
        """Scrapes results from cars.com.
        Args:
            car_dict:
        Returns:
            resultz: dict of DriftCars, keys are make_model
        """
        url_targets = gen_carscom_urls(input_dict=self.cardict, zarg=False)
        temp = scrape_carscom(url_targets)
        results = process_carscom(temp=temp, car_dict=car_dict)
        # convert results, a dict of dictionaries, into resultz, a dict of DriftCars
        resultz = dict.fromkeys(results.keys())
        for car in results.keys():
            print("Processing " + car)
            resultz[car] = DriftCar(df=results[car], source="carscom")
        return resultz

    def scrape_edmunds(self, car_dict: dict) -> dict:
        """Scrapes results from edmunds.com.
        Args:
            car_dict:
        """
        # TODO
        pass
