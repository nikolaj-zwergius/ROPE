import numpy as np
from pathlib import Path
class StructuralElement():
    """Base state and parser contract for PDB-backed structural elements.

    Concrete subclasses implement :meth:`_generate_cords` and return the start
    sugar, per-residue coordinates and source lines, final sugar, atom
    dictionaries, and source-file status consumed by :meth:`generate_cords`.
    """

    def __init__(self, name: str, file: str | Path, symbol: str) -> None:
        self.name = name
        self.file = file
        self.start_cord:np.ndarray = np.ndarray((0,0))
        self.build_cords:list[np.ndarray] = [np.ndarray((0,0))]
        self.build_lines:list[list[str]] = []
        self.last_coord: np.ndarray | None = None
        self.coord_dic: None = None
        self.symbol = symbol
    
    def generate_cords(self) -> None:
        self.start_cord,self.build_cords,self.build_lines,self.last_coord,self.coord_dict,self.file_found = self._generate_cords()

    def _generate_cords(
        self,
    ) -> tuple[
        np.ndarray,
        list[np.ndarray],
        list[list[str]],
        np.ndarray,
        list[dict[str, tuple[float, float, float]]],
        bool,
    ]:
        """Parse structural data; subclasses must provide the file format logic.

        Returns:
            Start coordinates, coordinates and source lines for each residue,
            final-residue coordinates, atom-coordinate dictionaries, and a
            flag indicating whether the source file was found.

        Raises:
            NotImplementedError: If called on the base class.
        """
        raise NotImplementedError
