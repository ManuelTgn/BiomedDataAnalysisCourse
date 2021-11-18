from numpy import pi
from utils import(
    exception_handler,
    check_type,
    PATID_START,
    T
)

from typing import List, Iterator, Dict

import pandas as pd
import os


class Patient():
    def __init__(self, patid: int, age: str, sex: str, pat_status: str) -> None:
        check_type(int, patid)
        if patid <= 99999:
            errmsg = f"Forbidden  patient ID ({patid})"
            exception_handler(ValueError, errmsg, False)
        check_type(str, age)
        check_type(str, sex)
        check_type(str, pat_status)
        self._patid = patid
        self._age = age
        self._sex = sex
        self._pat_status = pat_status


    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} object: {os.stat(self).st_size} bytes required>"
    

    def __str__(self) -> str:
        return str(
            f"PID: {self.patid}\n"
            f"\t- age:\t{self.age}\n"
            f"\t- sex:\t{self.sex}\n"
            f"\t- outcome:\t{self.pat_status}\n"
        )
    

    def _get_patid(self) -> int:
        """(PRIVATE)"""
        return self._patid
    
    @property
    def patid(self) -> int:
        return self._get_patid()

    
    def _get_age(self) -> str:
        """(PRIVATE)"""
        return self._age

    @property
    def age(self) -> str:
        return self._get_age()

    def _get_sex(self) -> str:
        """(PRIVATE)"""
        return self._sex

    @property
    def sex(self) -> str:
        return self._get_sex()


    def _get_pat_status(self) -> str:
        """(PRIVATE)"""
        return self._pat_status

    @property
    def pat_status(self) -> str:
        return self._get_pat_status()


class Patients(Dict[int, Patient]):
    _group = "Unknown"  # patients group type 

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} object: {len(self.values())}, {os.stat(self).st_size} bytes>"

    
    def __len__(self) -> int:
        return len(self.values())

    
    def __iter__(self) -> Iterator[Patient]:
        return PatientsIterator(self)

    
    def add(self, pid: int, patient: Patient) -> None:
        check_type(int, pid)
        check_type(Patient, patient)
        if pid < PATID_START: 
            errmsg = f"Forbidden patient ID ({pid})"
            exception_handler(ValueError, errmsg, False)
        try:
            self[pid] = patient
        except KeyError as e:
            errmsg = f"Wrong key ({pid})"
            exception_handler(e, errmsg, False)


    def set_group(self, group: str) -> None:
        check_type(str, group)
        self._group = group


    def _get_patients(self) -> List[Patient]:
        return list(self.values())

    @property
    def patients(self) -> List[Patient]:
        return self._get_patients()

    
    def _get_group(self) -> str:
        assert self._group
        return self._group

    @property
    def group(self) -> str:
        return self._get_group()


class PatientsIterator():
    def __init__(self, patients: Patients) -> None:
        check_type(Patients, patients)
        self._patients = list(patients.values())
        self._index = 0

    def __next__(self) -> Patient:
        if self._index < len(self._patients):
            pat = self._patients[self._index]
            self._index += 1
            assert isinstance(pat, Patient)
            return pat
        raise StopIteration


def initialize_patient(row: List[T], patid: int) -> Patient:
    patid += PATID_START
    age = row["Age.at.diagnosis"]
    sex = row["Sex"]
    status = row["Last.known.patient.status"]
    patient = Patient(patid, age, sex, status)
    return patient


def build_patients_dict(
    dataset: pd.DataFrame, 
    verbose: bool, 
    debug: bool
) -> Dict[int, Patient]:
    check_type(pd.DataFrame, dataset, debug)
    patslist = dataset.apply(lambda x : initialize_patient(x, x.name), axis=1)
    patsdict = {patient.patid:patient for patient in patslist}
    return patsdict


def build_patients_ds(
    dataset: pd.DataFrame,
    verbose: bool,
    debug: bool
) -> Patients:
    check_type(pd.DataFrame, dataset, debug)
    patients = Patients()
    patslist = dataset.apply(lambda x : initialize_patient(x, x.name), axis=1)
    for pat in patslist: patients[pat.patid] = pat
    return patients

   