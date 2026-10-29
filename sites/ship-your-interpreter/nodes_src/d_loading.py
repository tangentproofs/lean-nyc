NODES = []
def node(id, title, summary, body, quiz, caveats=(), widgets=None):
    NODES.append(dict(id=id, title=title, summary=summary, body=body, quiz=quiz, caveats=list(caveats), widgets=widgets))
def q(text, choices, answer, explain):
    return {"q": text, "type": "choice", "choices": choices, "answer": answer, "explain": explain}

# ---------------------------------------------------------------- C. loading

node("Vsa.MemRepr.ProgramRepr",
 "The AST as C structs in memory",
 "ProgramRepr m a n p says memory m holds, at address a, an array of n pointers to Stmt structs that encode exactly the program p, following the field offsets and tag numbers of c/src/ast.h. This is how the theorem names ‘the program’ inside the machine.",
 r"""## Plain English

**Definitions (Vsa/MemRepr.lean lines 46–205).** Memory is read little-endian, byte by byte
(`readLE`, `read32`, `read64`, lines 10–22). Strings are NUL-terminated and must be 7-bit ASCII (`CStr`,
lines 24–32). Then one inductive relation per AST type follows the C layout:

- an **expression** at address `a` has its kind tag (`EX_INT` = 0, …, `EX_FN` = 10) as a 32-bit value at `a`,
  and its payload in the union at `a + 8`: an int64, a string pointer, child pointers, an argument array
  with its count, and so on (`ExprRepr`, lines 46–112);
- a **statement** is the same, with tags `ST_EXPR` = 0, …, `ST_CONTINUE` = 8 (`StmtRepr`, lines 128–181);
- optional parts are null pointers (lines 183–193);
- a **statement array** is `n` consecutive 8-byte pointers (lines 195–200).

**`ProgramRepr m a n p`** (lines 204–205): the statement array at `a` has `n` entries encoding `p`, and `n` is
the length of `p`.

This is the only place the WHILE AST meets bytes. The C parser's job is to produce memory satisfying
this relation, but the theorem does not prove the parser does that. It assumes the AST is there.
""",
 [q("Which C header does this relation mirror?",
    ["c/src/ast.h", "c/src/value.h", "None; it is abstract"], 0,
    "The tag numbers and offsets match the enums and unions of c/src/ast.h."),
  q("What does ProgramRepr m a n p require about n?",
    ["n equals the length of p, and the array at a has n entries", "n is the number of bytes", "Nothing"], 0,
    "Vsa/MemRepr.lean lines 204–205."),
  q("Can a string in the AST contain non-ASCII bytes?",
    ["No. CStr requires each byte below 128", "Yes"], 0,
    "Vsa/MemRepr.lean lines 24–29."),
 ])

node("Vsa.Sim.LayoutInstance.InterpRunReadyFacts",
 "The machine is ready at interp_run",
 "What a configuration must satisfy: PC at interp_run, argument registers, ELF code and data present, runtime, console and heap initialised, stack geometry, plus the stack-admissibility assumption about the program.",
 r"""## Plain English

**Structures (Vsa/Sim/LayoutInstance.lean lines 40–99 and 183–197).** For a configuration `c`, a statement
array at `stmts` with `count` entries, and some auxiliary data (the interpreter object `inp`, native
function addresses `N`, an arena `A`, address maps for frames and closures):

**Physical facts** (`InterpRunPhysicalFacts`, lines 40–99), among others:

- the PC is `0x800043ec`, the entry of `interp_run` in the committed ELF, and `ra` is the return address in
  `main`;
- `a0`–`a3` hold the interpreter object, `stmts`, `count` and `repl_mode = 0`, and `sp` and `gp` have
  their entry values;
- the ELF's `.text`, `.rodata` and static data are in memory byte for byte (`text_image`, `rodata_image`,
  `statics`);
- the console and exit runtime data are initialised, and the output so far is empty;
- the global frame of the interpreter holds `print`, `println` and `assert` (`store`), and that stays true
  outside the interpreter's write footprint;
- the stack occupies `0x87800000`–`0x88000000` and every stack byte is present.

**Readiness** (`InterpRunReadyFacts`, lines 183–197) adds:

- `boot`: the dlmalloc-style heap is in its initial state, with ownership data and the
  [capacity](#/node/Vsa.Sim.DlHeap.InitialAllocatorAt) assumption;
- **`stack_admissible`**: any program laid out at `stmts` passes the static stack check `ProgramStackFits`
  (lines 105–124);
- all 31 general registers are defined, and `s0` has a specific value.

`InterpRunReady c stmts count` (lines 199–202) says such auxiliary data exists.
""",
 [q("Where must the PC be?",
    ["At interp_run's entry, 0x800043ec", "At the ELF's reset vector", "Anywhere in .text"], 0,
    "Vsa/Sim/LayoutInstance.lean line 26 and the pc field at line 46."),
  q("Which two fields are assumptions about the program rather than about the boot state?",
    ["capacity (inside boot) and stack_admissible", "pc and sp", "text_image and rodata_image"], 0,
    "Vsa/Sim/LayoutInstance.lean lines 189–193 and Vsa/Sim/DlHeap.lean lines 108–110."),
  q("Does this structure require the ELF's code to be in memory?",
    ["Yes: text_image and rodata_image", "No"], 0,
    "Vsa/Sim/LayoutInstance.lean lines 71–73."),
 ],
 caveats=["This is a long hypothesis, and its exact contents matter. The kernel checks that it holds at ten concrete traced states (Vsa/Sim/Boot/Gen/), but not that the real boot of the ELF reaches such a state. See Trust."])

node("Vsa.Sim.DlHeap.InitialAllocatorAt",
 "The heap starts empty enough (the capacity assumption)",
 "Besides describing the allocator's initial chunk and bin layout, InitialAllocatorAt contains capacity: for every terminating run of the loaded program with allocation cost n, twice n plus 8,256 bytes fits between the heap top and the heap end. This is an assumption about the program, not a theorem.",
 r"""## Plain English

**Structure (`InitialAllocatorAt`, Vsa/Sim/DlHeap.lean lines 104–110).**

- `heap`: the allocator's in-memory data describe a well-formed heap (`HeapAt`, earlier in the file):
  a chunk walk up to `top`, bins of free chunks, the bin bitmap, and the program break.
- **`capacity`**: for every program `p` laid out at the statement array and every
  [cost-annotated](#/node/Vsa.While.ExecSeqCost) normal run of `p` with cost `n`, `2·n + extendSlack ≤ heapEnd − top`,
  where `extendSlack` is 8192 + 64 bytes (line 102).

The factor 2 and the slack cover allocator overheads, such as chunk headers and rounding, that the
proof charges against the budget.

Capacity is what lets the total proof show that `malloc` never returns null on a terminating run.
[endToEnd_checked](#/node/Vsa.Sim.EndToEnd.endToEnd_checked) replaces it with a computed bound,
`interpCostBound`, and a check on the heap size.
""",
 [q("Is capacity proved or assumed in endToEnd_refinement?",
    ["Assumed, as part of Loaded", "Proved from the ELF"], 0,
    "It is a field of the hypothesis (Vsa/Sim/DlHeap.lean lines 108–110 via Vsa/Sim/LayoutInstance.lean lines 189–191)."),
  q("What does capacity bound?",
    ["Twice the allocation cost of any terminating run, plus slack, by the free heap space", "The number of statements", "The stack depth"], 0,
    "Vsa/Sim/DlHeap.lean lines 108–110."),
  q("What happens to a program that would need more heap than available?",
    ["It is outside the theorem: Loaded cannot hold for it", "The theorem says it exits 0"], 0,
    "Without capacity, Loaded is false and the theorem says nothing. On the machine such a run would hit the out-of-memory path (exit 1)."),
 ])

node("Vsa.Refine.Loaded",
 "Loaded: program and machine fit together",
 "Loaded L p c says the AST of p is laid out at some address with some count, and the configuration satisfies the layout's readiness predicate at those arguments. With L = interpRunLayout, this is the only hypothesis of the main theorem.",
 r"""## Plain English

**Definitions (Vsa/Refinement.lean lines 9–13).** A **layout** is a predicate on a configuration and two
numbers: where the statement array is, and how long it is. **`Loaded L p c`** says there are such numbers
`a` and `n` with

- [ProgramRepr](#/node/Vsa.MemRepr.ProgramRepr) `c.σ.mem a n p`: the AST of `p` is in memory at `a`, and
- `L.atInterpRun c a n`: the machine is ready to run the interpreter on it.

For the concrete interpreter, `L` is [interpRunLayout](#/node/Vsa.Sim.LayoutInstance.interpRunLayout), whose
predicate is `InterpRunReady` ([details](#/node/Vsa.Sim.LayoutInstance.InterpRunReadyFacts)).

`Loaded` keeps the generic refinement argument ([Vsa.Refine.refinement](#/node/Vsa.Refine.refinement)) apart
from the specifics of this ELF. Another interpreter on the same machine supplies its own layout
(docs/PORTING.md).
""",
 [q("What two things does Loaded combine?",
    ["The AST in memory (ProgramRepr) and the layout's readiness predicate", "Type checking and parsing", "Heap and stack"], 0,
    "Vsa/Refinement.lean lines 12–13."),
  q("Which layout does the main theorem use?",
    ["interpRunLayout", "An arbitrary layout"], 0,
    "VsaIris/Interp/EndToEnd.lean line 160."),
  q("Is the heap-capacity assumption visible in the statement of Loaded?",
    ["Not directly; it is buried in interpRunLayout's readiness predicate", "Yes, it is a separate argument"], 0,
    "Vsa/Sim/LayoutInstance.lean lines 189–191 and 204–205."),
 ])

node("Vsa.Sim.LayoutInstance.interpRunLayout",
 "interpRunLayout: the concrete layout",
 "interpRunLayout is the layout whose readiness predicate is InterpRunReady: the machine is at interp_run of the committed ELF with all the boot facts, the initial heap, and the program assumptions.",
 r"""## Plain English

**Definition (`interpRunLayout`, Vsa/Sim/LayoutInstance.lean lines 204–205).** The layout for
[Loaded](#/node/Vsa.Refine.Loaded) whose predicate, for a configuration and a statement array at `a` with `n`
entries, is `InterpRunReady c a n` (lines 199–202). That predicate says suitable auxiliary data exist
making [InterpRunReadyFacts](#/node/Vsa.Sim.LayoutInstance.InterpRunReadyFacts) hold.

Every address in it (`0x800043ec`, `0x87fffd00`, `0x8001b510`, …) is specific to the committed
`c/while-riscv-htif.elf`. A rebuild of the C code with another toolchain would need a new layout and new
proofs.
""",
 [q("Is interpRunLayout generic across builds of the C code?",
    ["No. It names addresses in the committed ELF", "Yes"], 0,
    "Vsa/Sim/LayoutInstance.lean lines 26–32 fix addresses; the README warns that a rebuild can change the bytes."),
  q("What is its readiness predicate?",
    ["InterpRunReady", "ProgramRepr"], 0,
    "Vsa/Sim/LayoutInstance.lean line 205."),
  q("Does it include the stack-admissibility assumption?",
    ["Yes, inside InterpRunReadyFacts", "No"], 0,
    "Vsa/Sim/LayoutInstance.lean line 193."),
 ])
