from utils import(
    exception_handler,
    check_type,
    NO_GROUP,
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


class Patients():
    def __init__(self, pats_list: List[Patient], group_name: str = NO_GROUP) -> None:
        check_type(list, pats_list)
        check_type(str, group_name)
        self._pats_list = pats_list
        self._group_name = group_name
        self._size = len(self.pats_list)
    
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} object: {os.stat(self).st_size} bytes>"

    
    def __str__(self) -> str:
        return f"List of {len(self)} patients (group {self.group_name})"

    
    def __len__(self) -> int:
        return len(self._pats_list)

    
    def __iter__(self) -> Iterator[Patient]:
        return PatientsIterator(self)

    
    def __getitem__(self, idx: int) -> Patient:
        assert bool(self.pats_list)
        try:
            pat = self.pats_list[idx]
        except IndexError as e:
            errmsg = f"Index out of bounds ({idx})"
            exception_handler(e, errmsg, False)
        return pat


    def _get_pats_list(self) -> List[Patient]:
        return self._pats_list

    @property
    def pats_list(self) -> List[Patient]:
        return self._get_pats_list()

    
    def _get_group_name(self) -> str:
        if self._group_name == NO_GROUP:
            return ""
        return self._group_name

    @property
    def group_name(self) -> str:
        return self._get_group_name()

    
    def append(self, patient: Patient) -> None:
        check_type(Patient, patient)
        self._pats_list.append(patient)


class PatientsIterator():
    def __init__(self, patients: Patients) -> None:
        check_type(Patients, patients)
        self._patients = patients
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

   