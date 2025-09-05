"""|NumberingPart| and closely related objects."""

from typing import Self

from ..opc.part import XmlPart
from ..shared import lazyproperty


class NumberingPart(XmlPart):
    """Proxy for the numbering.xml part containing numbering definitions for a document
    or glossary."""

    @classmethod
    def new(cls) -> Self:
        """Return newly created empty numbering part, containing only the root
        ``<w:numbering>`` element."""
        raise NotImplementedError

    @lazyproperty
    def numbering_definitions(self):
        """The |_NumberingDefinitions| instance containing the numbering definitions
        (<w:num> element proxies) for this numbering part."""
        return _NumberingDefinitions(self._element)

    def get_abstract_by_num_id(self, num_id: int):
        for num in self._element.num_lst:
            if num.numId != num_id:
                continue

            num_abs_num_id = num.abstractNumId.val
            for abs_num in self._element.abstractNum_lst:
                if num_abs_num_id != abs_num.abstractNumId:
                    continue

                return abs_num

    def get_lvl(self, num_id: int, ilvl: int):
        abs_num = self.get_abstract_by_num_id(num_id)
        ilvl_ovr = self.get_ilvl_override(num_id, ilvl)
        if ilvl_ovr is not None:
            ilvl = ilvl_ovr

        for lvl in abs_num.lvl_lst:
            if ilvl != lvl.ilvl:
                continue

            return lvl

    def get_ilvl_override(self, num_id: int, ilvl: int):
        for num in self._element.num_lst:
            if num.numId != num_id:
                continue

            for ovr in num.lvlOverride_lst:
                print(ovr.ilvl)
                if ovr.ilvl is None or ovr.ilvl != ilvl:
                    continue

                return ovr.startOverride.val

class _NumberingDefinitions:
    """Collection of |_NumberingDefinition| instances corresponding to the ``<w:num>``
    elements in a numbering part."""

    def __init__(self, numbering_elm):
        super(_NumberingDefinitions, self).__init__()
        self._numbering = numbering_elm

    def __len__(self):
        return len(self._numbering.num_lst)
