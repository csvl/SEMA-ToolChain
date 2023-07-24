import angr
from .open import open

import logging

lw = logging.getLogger("CustomSimProcedureLinux")
logging.getLogger("CustomSimProcedureLinux").setLevel("INFO")

class opendir(angr.SimProcedure):
    def run(self, fname):
        lw.info(self.cc)
        p_open = self.inline_call(open, fname, 0o200000, 0)  # O_DIRECTORY
        # using the same hack we used to use for fopen etc... using the fd as a pointer
        print("Tried to open directory: " + fname + ". Returned file descriptor: " + str(p_open.ret_expr))
        return p_open.ret_expr

# import angr
# import logging

# lw = logging.getLogger("CustomSimProcedureLinux")
# logging.getLogger("CustomSimProcedureLinux").setLevel("INFO")

# from collections import namedtuple

# Dirent = namedtuple("dirent", ("d_ino", "d_off", "d_reclen", "d_type", "d_name"))


# class opendir(angr.SimProcedure):
#     struct = None
#     condition = None

#     def run(self, dirp):  # pylint: disable=arguments-differ
#         # TODO: make sure argument is actually a DIR struct
#         if self.state.arch.name != "AMD64":
#             lw.error("readdir SimProcedure is only implemented for AMD64")
#             return 0

#         self._build_amd64()
#         self.instrument()
#         malloc = angr.SIM_PROCEDURES["libc"]["malloc"]
#         pointer = self.inline_call(malloc, 19 + 256).ret_expr
#         self._store_amd64(pointer)
#         return self.state.solver.If(self.condition, pointer, 0)

#     def instrument(self):
#         """
#         Override this function to instrument the SimProcedure.

#         The two useful variables you can override are self.struct, a named tuple of all the struct
#         fields, and self.condition, the condition for whether the function succeeds.
#         """
#         pass

#     def _build_amd64(self):
#         self.struct = Dirent(
#             self.state.solver.BVV(0, 64),  # d_ino
#             self.state.solver.BVV(0, 64),  # d_off
#             self.state.solver.BVS("d_reclen", 16, key=("api", "readdir", "d_reclen")),  # d_reclen
#             self.state.solver.BVS("d_type", 8, key=("api", "readdir", "d_type")),  # d_type
#             self.state.solver.BVS("d_name", 255 * 8, key=("api", "readdir", "d_name")),
#         )  # d_name
#         self.condition = self.state.solver.BoolS("readdir_cond")  # TODO: variable key

#     def _store_amd64(self, ptr):
#         def stores(offset, val):
#             return self.state.memory.store(ptr + offset, val, endness="Iend_BE")

#         def storei(offset, val):
#             return self.state.memory.store(ptr + offset, val, endness="Iend_LE")

#         storei(0, self.struct.d_ino)
#         storei(8, self.struct.d_off)
#         storei(16, self.struct.d_reclen)
#         storei(18, self.struct.d_type)
#         stores(19, self.struct.d_name)
#         stores(19 + 255, self.state.solver.BVV(0, 8))