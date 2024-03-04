# from __future__ import annotations
#
# from enum import Enum, auto
# from typing import Optional
#
# from fastuipr import AnyComponent, components as c
#
# from pawsupport.fastui_ps import DFLT_CSS
#
#
#
# class DivPR(c.Div):
#
#     def __init__(
#             self,
#             components: List[AnyComponent],
#             class_name: str = CSSEnum.PLAIN,
#             col: RowColType = '',
#             row: RowColType = '',
#     ):
#         if all([col, row]):
#             # or can we?
#             raise ValueError("Cannot have both col and row set")
#
#         if col == 'one':
#             components = Col.from_list(components)
#         elif col == 'many':
#             components = Col.from_list_many(components)
#
#         if row == 'one':
#             components = Row.from_list(components)
#         elif row == 'many':
#             components = Row.from_list_many(components)
#
#         super().__init__(components=components, class_name=class_name)
#
#     @classmethod
#     def empty(cls, col: RowColType = '', row: RowColType = '') -> DivPR:
#         return cls(components=[c.Text(text="---")], col=col, row=row)
#
#     @classmethod
#     def from_list_many(cls, components: List[AnyComponent], class_name: str = '', ) -> List[DivPR]:
#         return [cls(components=[comp], row_class_name=class_name) for comp in components]
#
#     @classmethod
#     def from_list(cls, components: List[AnyComponent], class_name: str = '') -> DivPR:
#         return cls(components=components, row_class_name=class_name)
#
#
# class Row(DivPR):
#
#     def __init__(
#             self,
#             components: List[AnyComponent],
#             row_class_name: str = CSSEnum.ROW,
#             sub_cols: RowColType = '',
#             col_class_name=''
#     ):
#         row_class_name = f"row {row_class_name}"
#         if not components:
#             components = [DivPR.empty()]
#         # if sub_cols:
#         #     components = Col.from_list_many(components, class_name=col_class_name)
#         super().__init__(components=components, class_name=row_class_name, col=sub_cols)
#
#     @classmethod
#     def from_list_many(cls, components: List[AnyComponent], class_name: str = '') -> List[DivPR]:
#         return [cls(components=[comp], row_class_name=class_name) for comp in components]
#
#     @classmethod
#     def from_list(cls, components: List[AnyComponent], class_name: str = '') -> DivPR:
#         return cls(components=components, row_class_name=class_name)
#
#
# class Col(DivPR):
#
#     def __init__(
#             self,
#             components: List[AnyComponent],
#             col_class: str = CSSEnum.COL,
#             sub_rows: RowColType = '',
#             row_class: str = CSSEnum.1
#     ):
#         col_class = f"col {col_class}"
#         if not components:
#             components = [DivPR.empty()]
#         # if sub_rows:
#         #     components = Row.from_list_many(components, class_name=row_class)
#         super().__init__(components=components, class_name=col_class, row=sub_rows)
#
#     @classmethod
#     def from_list_many(cls, components: List[AnyComponent], class_name: str = CSSEnum.COL) -> \
#             List[
#                 Col]:
#         return [cls(components=[comp], col_class=class_name) for comp in components]
#
#     @classmethod
#     def from_list(cls, components: List[AnyComponent], class_name: str = CSSEnum.COL) -> DivPR:
#         return cls(components=components, col_class=class_name)
#
#     # @classmethod
#     # def empty(cls):
#     #     return cls(components=[DivPR.empty()])
