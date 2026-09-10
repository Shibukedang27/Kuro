
#!/usr/bin/env python3
from dataclasses import dataclass
import sys, re

TYPES = {"Integers", "Decimals", "Text", "Symbols"}

class KuroError(Exception): pass
class KuroLexError(KuroError): pass
class KuroParseError(KuroError): pass
class KuroSemanticError(KuroError): pass
class KuroRuntimeError(KuroError): pass

@dataclass
class Tok:
    kind:str; value:str; line:int; col:int

@dataclass
class S:
    line:int; col:int
@dataclass
class Decl(S): name:str; typ:str
@dataclass
class Assign(S): name:str; values:list
@dataclass
class Input(S): names:list
@dataclass
class Add(S): value:object; target:str
@dataclass
class Update(S): name:str; value:object
@dataclass
class Print(S): value:object
@dataclass
class Get(S): target:str; index:object
@dataclass
class Length(S): target:str
@dataclass
class Set(S): target:str; index:object; value:object
@dataclass
class Compare(S): name:str; left:object; op:str; right:object
@dataclass
class If(S): left:object; op:str; right:object; then_body:list; else_body:list
@dataclass
class Repeat(S): count:object; body:list
@dataclass
class Action(S): name:str; args:list; body:list
@dataclass
class Return(S): value:object
@dataclass
class Call(S): name:str; args:list

def strip_comments(line):
    out=[]; i=0; quoted=False
    while i<len(line):
        c=line[i]
        if c=='"':
            quoted=not quoted; out.append(c); i+=1; continue
        if not quoted and c=='#': break
        if not quoted and c=='/' and i+1<len(line) and line[i+1]=='/': break
        out.append(c); i+=1
    return ''.join(out)

def lex(src):
    toks=[]
    for ln, raw in enumerate(src.splitlines(),1):
        s=strip_comments(raw); i=0
        while i<len(s):
            c=s[i]
            if c.isspace(): i+=1; continue
            col=i+1
            if c=='"':
                start=i; i+=1; b=[]
                while i<len(s):
                    if s[i]=='"':
                        i+=1; toks.append(Tok("STRING","".join(b),ln,col)); break
                    if s[i]=='\\' and i+1<len(s):
                        mp={'n':'\n','t':'\t','r':'\r','"':'"','\\':'\\'}
                        b.append(mp.get(s[i+1],s[i+1])); i+=2
                    else: b.append(s[i]); i+=1
                else: raise KuroLexError(f"{ln}:{col}: unterminated string")
                continue
            if c.isdigit():
                st=i; dot=False
                while i<len(s) and (s[i].isdigit() or (s[i]=='.' and not dot)):
                    dot |= s[i]=='.'; i+=1
                toks.append(Tok("NUMBER",s[st:i],ln,col)); continue
            if c.isalpha() or c=='_':
                st=i; i+=1
                while i<len(s) and (s[i].isalnum() or s[i]=='_'): i+=1
                toks.append(Tok("WORD",s[st:i],ln,col)); continue
            if c in '=,;.()@':
                toks.append(Tok(c,c,ln,col)); i+=1; continue
            raise KuroLexError(f"{ln}:{col}: unexpected character {c!r}")
    toks.append(Tok("EOF","",len(src.splitlines())+1,1))
    return toks

class Parser:
    def __init__(self,toks): self.t=toks; self.i=0
    def c(self): return self.t[self.i]
    def peek(self,n=1): return self.t[min(self.i+n,len(self.t)-1)]
    def adv(self): x=self.c(); self.i+=1; return x
    def err(self,msg,t=None): t=t or self.c(); raise KuroParseError(f"{t.line}:{t.col}: {msg}")
    def isw(self,w): return self.c().kind=="WORD" and self.c().value==w
    def takew(self,w):
        if not self.isw(w): self.err(f"expected {w!r}, got {self.c().value!r}")
        return self.adv()
    def word(self):
        if self.c().kind!="WORD": self.err("expected a word")
        return self.adv().value
    def value(self):
        t=self.c()
        if t.kind=="STRING": self.adv(); return ("lit",t.value)
        if t.kind=="NUMBER":
            self.adv(); return ("lit",float(t.value) if "." in t.value else int(t.value))
        if t.kind=="@":
            self.adv(); return ("var",self.word())
        if t.kind=="WORD":
            self.adv(); return ("word",t.value)
        self.err("expected a value",t)
    def op(self):
        if self.isw("greater"):
            self.adv(); self.takew("than"); return "gt"
        if self.isw("less"):
            self.adv(); self.takew("than"); return "lt"
        if self.isw("equal"):
            self.adv()
            if self.isw("to"): self.adv()
            return "eq"
        if self.isw("equals"):
            self.adv()
            if self.isw("to"): self.adv()
            return "eq"
        if self.isw("not"):
            self.adv(); self.takew("equal")
            if self.isw("to"): self.adv()
            return "ne"
        self.err("invalid comparison operator")
    def parse(self): return self.block(set())
    def block(self, stops):
        out=[]
        while self.c().kind!="EOF":
            if self.c().kind=="WORD" and self.c().value in stops: break
            out.append(self.stmt())
        return out
    def vals(self):
        a=[self.value()]
        while self.c().kind==",": self.adv(); a.append(self.value())
        self.expect(";")
        return a
    def expect(self,k):
        if self.c().kind!=k: self.err(f"expected {k!r}, got {self.c().value!r}")
        return self.adv()
    def stmt(self):
        t=self.c()
        # declaration: Name is Text;
        if (t.kind=="WORD" and self.peek().kind=="WORD" and self.peek().value=="is"
            and not (self.peek(2).kind=="WORD" and self.peek(2).value in
                     {"greater","less","equal","equals","not"})):
            name=self.word(); self.takew("is"); typ=self.word(); self.expect(";")
            return Decl(t.line,t.col,name,typ)
        if self.isw("Take"):
            self.adv()
            if self.isw("user"): self.adv()
            names=[self.word()]
            while self.isw("and"): self.adv(); names.append(self.word())
            self.expect(";"); return Input(t.line,t.col,names)
        if self.isw("Print"):
            self.adv(); v=self.value(); self.expect("."); return Print(t.line,t.col,v)
        if self.isw("Add"):
            self.adv(); v=self.value(); self.takew("to"); n=self.word(); self.expect(";")
            return Add(t.line,t.col,v,n)
        if self.isw("Update"):
            self.adv(); n=self.word(); self.takew("to"); v=self.value(); self.expect(";")
            return Update(t.line,t.col,n,v)
        if self.isw("Get"):
            self.adv(); n=self.word(); idx=None if self.c().kind==";" else self.value(); self.expect(";")
            return Get(t.line,t.col,n,idx)
        if self.isw("Length"):
            self.adv(); n=self.word(); self.expect(";"); return Length(t.line,t.col,n)
        if self.isw("Set"):
            self.adv(); n=self.word(); idx=self.value(); self.takew("to"); v=self.value(); self.expect(";")
            return Set(t.line,t.col,n,idx,v)
        if self.isw("Compare"):
            self.adv(); n=self.word(); left=self.value(); op=self.op(); right=self.value(); self.expect(";")
            return Compare(t.line,t.col,n,left,op,right)
        if self.isw("If"):
            self.adv(); left=self.value(); self.takew("is"); op=self.op(); right=self.value(); self.expect(";")
            tb=self.block({"Else","Done"}); eb=[]
            if self.isw("Else"):
                self.adv(); self.expect(";"); eb=self.block({"Done"})
            self.takew("Done"); self.expect(".")
            return If(t.line,t.col,left,op,right,tb,eb)
        if self.isw("Repeat"):
            self.adv(); count=self.value(); self.expect(";"); body=self.block({"Done"})
            self.takew("Done"); self.expect("."); return Repeat(t.line,t.col,count,body)
        if self.isw("Action"):
            self.adv(); name=self.word(); self.expect("("); args=[]
            if self.c().kind!=")":
                args=[self.word()]
                while self.c().kind==",": self.adv(); args.append(self.word())
            self.expect(")"); self.expect(";"); body=self.block({"Done"})
            self.takew("Done"); self.expect("."); return Action(t.line,t.col,name,args,body)
        if self.isw("Return"):
            self.adv(); v=self.value(); self.expect(";"); return Return(t.line,t.col,v)
        if self.isw("Call"):
            self.adv(); n=self.word(); self.expect("("); args=[]
            if self.c().kind!=")":
                args=[self.value()]
                while self.c().kind==",": self.adv(); args.append(self.value())
            self.expect(")"); self.expect(";"); return Call(t.line,t.col,n,args)
        # legacy one-line condition kept for backwards compatibility
        if self.isw("Entered"):
            self.adv(); left=self.word(); self.takew("is"); op=self.op(); right=self.value()
            self.takew("then")
            if not self.isw("Print"): self.err("expected Print after then")
            self.adv(); tv=self.value(); self.takew("otherwise")
            if not self.isw("Print"): self.err("expected Print after otherwise")
            self.adv(); fv=self.value(); self.expect(";")
            return If(t.line,t.col,("var",left),op,right,[Print(t.line,t.col,tv)],[Print(t.line,t.col,fv)])
        if t.kind=="WORD" and self.peek().kind=="=":
            n=self.word(); self.expect("="); return Assign(t.line,t.col,n,self.vals())
        self.err(f"unknown statement starting with {t.value!r}")

def lit(v):
    if v[0] in ("lit","word"): return v[1]
    raise ValueError

def type_of(x):
    if isinstance(x,bool): return "Symbols"
    if isinstance(x,int) and not isinstance(x,bool): return "Integers"
    if isinstance(x,float): return "Decimals"
    if isinstance(x,str): return "Text"
    if isinstance(x,list):
        return type_of(x[0]) if x else "Text"
    return "Symbols"

def compatible(declared,x):
    return declared==type_of(x) or (declared=="Decimals" and type_of(x)=="Integers")

def resolve(v,env,locals_):
    if v[0]=="lit": return v[1]
    if v[0]=="word":
        if v[1] in locals_: return locals_[v[1]]
        if v[1] in env: return env[v[1]]
        return v[1]
    n=v[1]
    if n in locals_: return locals_[n]
    if n in env: return env[n]
    raise KuroRuntimeError(f"undefined value {n!r}")

def cmp(a,b,op):
    return {"gt":a>b,"lt":a<b,"eq":a==b,"ne":a!=b}[op]

class Engine:
    def __init__(self,ast):
        self.ast=ast; self.env={}; self.types={}; self.actions={}; self.ir=[]; self.result=None
        self.collect(ast)
    def collect(self,body):
        for s in body:
            if isinstance(s,Action):
                if s.name in self.actions: raise KuroSemanticError(f"{s.line}:{s.col}: duplicate action {s.name!r}")
                if len(set(s.args))!=len(s.args): raise KuroSemanticError(f"{s.line}:{s.col}: duplicate action parameter")
                self.actions[s.name]=s
    def checkval(self,v,line,known=None):
        if v[0]=="var" and v[1] != "_" and v[1] not in self.types and v[1] not in (known or set()):
            raise KuroSemanticError(f"{line}: undefined value {v[1]!r}")
    def sem(self,body,in_action=False,locals_=set()):
        for s in body:
            if isinstance(s,Decl):
                # Already collected by semantic(); validate only.
                if s.typ not in TYPES:
                    raise KuroSemanticError(f"{s.line}:{s.col}: unknown type {s.typ!r}")
            elif isinstance(s,Assign):
                if s.name in self.types:
                    for v in s.values:
                        if v[0] in ("lit","word") and not compatible(self.types[s.name],v[1]):
                            raise KuroSemanticError(f"{s.line}:{s.col}: cannot assign {type_of(v[1])} to {self.types[s.name]} variable {s.name!r}")
            elif isinstance(s,Input):
                for n in s.names:
                    if n not in self.types: raise KuroSemanticError(f"{s.line}:{s.col}: input variable {n!r} must be declared")
            elif isinstance(s,Add):
                if s.target not in self.types: raise KuroSemanticError(f"{s.line}:{s.col}: unknown variable {s.target!r}")
                if self.types[s.target] not in {"Integers","Decimals"}: raise KuroSemanticError(f"{s.line}:{s.col}: Add target must be numeric")
                self.checkval(s.value,s.line,locals_)
            elif isinstance(s,(Update,Print,Get,Length,Set,Compare,If,Repeat,Return,Call)):
                if isinstance(s,Update):
                    if s.name not in self.types and s.name not in locals_: raise KuroSemanticError(f"{s.line}:{s.col}: unknown variable {s.name!r}")
                    self.checkval(s.value,s.line,locals_)
                elif isinstance(s,Print): self.checkval(s.value,s.line,locals_)
                elif isinstance(s,Get):
                    if s.target not in self.types: raise KuroSemanticError(f"{s.line}:{s.col}: unknown target {s.target!r}")
                    if s.index: self.checkval(s.index,s.line,locals_)
                elif isinstance(s,Length):
                    if s.target not in self.types: raise KuroSemanticError(f"{s.line}:{s.col}: unknown target {s.target!r}")
                elif isinstance(s,Set):
                    if s.target not in self.types: raise KuroSemanticError(f"{s.line}:{s.col}: unknown target {s.target!r}")
                    self.checkval(s.index,s.line,locals_); self.checkval(s.value,s.line,locals_)
                elif isinstance(s,Compare):
                    self.checkval(s.left,s.line,locals_); self.checkval(s.right,s.line,locals_)
                    self.types.setdefault(s.name, "Symbols")
                    self.types.setdefault(s.name, "Symbols")
                elif isinstance(s,If):
                    self.checkval(s.left,s.line,locals_); self.checkval(s.right,s.line,locals_)
                    self.sem(s.then_body,in_action,locals_); self.sem(s.else_body,in_action,locals_)
                elif isinstance(s,Repeat):
                    self.checkval(s.count,s.line,locals_); self.sem(s.body,in_action,locals_|{"Index"})
                elif isinstance(s,Return):
                    if not in_action: raise KuroSemanticError(f"{s.line}:{s.col}: Return is only valid inside an Action")
                    self.checkval(s.value,s.line,locals_)
                elif isinstance(s,Call):
                    if s.name not in self.actions: raise KuroSemanticError(f"{s.line}:{s.col}: unknown action {s.name!r}")
                    need=len(self.actions[s.name].args)
                    if len(s.args)!=need: raise KuroSemanticError(f"{s.line}:{s.col}: action {s.name!r} expects {need} argument(s), got {len(s.args)}")
                    for a in s.args: self.checkval(a,s.line,locals_)
            elif isinstance(s,Action):
                self.sem(s.body,True,locals_|set(s.args))
    def semantic(self):
        # First collect explicit declarations, action signatures, and inferred variables.
        # Kuro permits simple assignment without a prior declaration.
        for st in self.ast:
            if isinstance(st, Decl):
                if st.typ not in TYPES:
                    raise KuroSemanticError(f"{st.line}:{st.col}: unknown type {st.typ!r}")
                if st.name in self.types:
                    raise KuroSemanticError(f"{st.line}:{st.col}: duplicate declaration {st.name!r}")
                self.types[st.name] = st.typ
            elif isinstance(st, Assign) and st.name not in self.types:
                vals = []
                for v in st.values:
                    if v[0] in ("lit","word"):
                        vals.append(type_of(v[1]))
                if vals:
                    if all(x == vals[0] for x in vals):
                        self.types[st.name] = vals[0]
        self.sem(self.ast)
    def emit(self,x): self.ir.append(x)
    def exec(self,body,locals_=None):
        locals_=locals_ or {}
        for s in body:
            r=self.exec1(s,locals_)
            if r is not None: return r
        return None
    def exec1(self,s,locals_):
        if isinstance(s,Decl): self.emit(f"TYPE {s.name} {s.typ}"); return
        if isinstance(s,Assign):
            vals=[resolve(v,self.env,locals_) for v in s.values]; self.env[s.name]=vals[0] if len(vals)==1 else vals
            self.emit(f"STORE {s.name}"); return
        if isinstance(s,Input):
            for n in s.names:
                raw=input(f"{n} ({self.types[n]}): "); typ=self.types[n]
                try: x=int(raw) if typ=="Integers" else float(raw) if typ=="Decimals" else raw
                except ValueError: raise KuroRuntimeError(f"invalid {typ} input for {n!r}")
                self.env[n]=x; self.emit(f"INPUT {n} {typ}")
            return
        if isinstance(s,Add):
            x=resolve(s.value,self.env,locals_); self.env[s.target]=self.env.get(s.target,0)+x; self.emit(f"ADD {s.target} {x}"); return
        if isinstance(s,Update):
            self.env[s.name]=resolve(s.value,self.env,locals_); self.emit(f"UPDATE {s.name}"); return
        if isinstance(s,Print):
            x=resolve(s.value,self.env,locals_)
            if isinstance(x,list):
                for y in x: print(y)
            else: print(x)
            self.emit("PRINT"); return
        if isinstance(s,Get):
            x=self.env[s.target]
            if s.index is None: y=x
            else:
                i=int(resolve(s.index,self.env,locals_))
                try: y=x[i]
                except Exception: raise KuroRuntimeError(f"index {i} out of range for {s.target!r}")
            self.env["_"]=y; print(y); self.emit(f"GET {s.target}"); return
        if isinstance(s,Length):
            try: y=len(self.env[s.target])
            except Exception: raise KuroRuntimeError(f"{s.target!r} has no length")
            self.env["_"]=y; print(y); self.emit(f"LENGTH {s.target}"); return
        if isinstance(s,Set):
            target=self.env[s.target]; i=int(resolve(s.index,self.env,locals_)); v=resolve(s.value,self.env,locals_)
            if isinstance(target,str):
                if not isinstance(v,str) or len(v)!=1: raise KuroRuntimeError("Set on Text requires one character")
                if not 0<=i<len(target): raise KuroRuntimeError("Text index out of range")
                self.env[s.target]=target[:i]+v+target[i+1:]
            elif isinstance(target,list):
                if not 0<=i<len(target): raise KuroRuntimeError("collection index out of range")
                self.env[s.target][i]=v
            else: raise KuroRuntimeError("Set target is not indexable")
            self.emit(f"SET {s.target} {i}"); return
        if isinstance(s,Compare):
            self.env[s.name]=cmp(resolve(s.left,self.env,locals_),resolve(s.right,self.env,locals_),s.op); self.emit(f"COMPARE {s.name} {s.op}"); return
        if isinstance(s,If):
            yes=cmp(resolve(s.left,self.env,locals_),resolve(s.right,self.env,locals_),s.op); self.emit(f"IF {s.op}")
            return self.exec(s.then_body,locals_) if yes else self.exec(s.else_body,locals_)
        if isinstance(s,Repeat):
            n=int(resolve(s.count,self.env,locals_))
            if n<0: raise KuroRuntimeError("Repeat count cannot be negative")
            old=self.env.get("Index",None)
            for i in range(n):
                self.env["Index"]=i; r=self.exec(s.body,locals_)
                if r is not None: break
            if old is None: self.env.pop("Index",None)
            else: self.env["Index"]=old
            self.emit(f"REPEAT {n}"); return
        if isinstance(s,Action): self.emit(f"ACTION {s.name}({','.join(s.args)})"); return
        if isinstance(s,Return): return resolve(s.value,self.env,locals_)
        if isinstance(s,Call):
            a=self.actions[s.name]; loc={p:resolve(v,self.env,locals_) for p,v in zip(a.args,s.args)}
            r=self.exec(a.body,loc); self.env["_"]=r; self.emit(f"CALL {s.name}"); return
    def run(self):
        self.semantic()
        self.exec([s for s in self.ast if not isinstance(s,Action)])
        print("\nKURO IR v0.4")
        print("----------------")
        for i,x in enumerate(self.ir): print(f"{i:04d}  {x}")

def compile_source(src):
    ast=Parser(lex(src)).parse(); e=Engine(ast); e.run(); return e

def main():
    if len(sys.argv)!=2:
        print("usage: python3 kuro.py <file.kuro>"); return 2
    try:
        compile_source(open(sys.argv[1],encoding="utf-8").read()); return 0
    except KuroError as e:
        print("KURO ERROR:",e,file=sys.stderr); return 1
if __name__=="__main__": raise SystemExit(main())
