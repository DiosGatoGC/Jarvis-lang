# Generated from JarvisLang.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .JarvisLangParser import JarvisLangParser
else:
    from JarvisLangParser import JarvisLangParser

# This class defines a complete listener for a parse tree produced by JarvisLangParser.
class JarvisLangListener(ParseTreeListener):

    # Enter a parse tree produced by JarvisLangParser#program.
    def enterProgram(self, ctx:JarvisLangParser.ProgramContext):
        pass

    # Exit a parse tree produced by JarvisLangParser#program.
    def exitProgram(self, ctx:JarvisLangParser.ProgramContext):
        pass


    # Enter a parse tree produced by JarvisLangParser#statement.
    def enterStatement(self, ctx:JarvisLangParser.StatementContext):
        pass

    # Exit a parse tree produced by JarvisLangParser#statement.
    def exitStatement(self, ctx:JarvisLangParser.StatementContext):
        pass


    # Enter a parse tree produced by JarvisLangParser#varDecl.
    def enterVarDecl(self, ctx:JarvisLangParser.VarDeclContext):
        pass

    # Exit a parse tree produced by JarvisLangParser#varDecl.
    def exitVarDecl(self, ctx:JarvisLangParser.VarDeclContext):
        pass


    # Enter a parse tree produced by JarvisLangParser#constDecl.
    def enterConstDecl(self, ctx:JarvisLangParser.ConstDeclContext):
        pass

    # Exit a parse tree produced by JarvisLangParser#constDecl.
    def exitConstDecl(self, ctx:JarvisLangParser.ConstDeclContext):
        pass


    # Enter a parse tree produced by JarvisLangParser#assignment.
    def enterAssignment(self, ctx:JarvisLangParser.AssignmentContext):
        pass

    # Exit a parse tree produced by JarvisLangParser#assignment.
    def exitAssignment(self, ctx:JarvisLangParser.AssignmentContext):
        pass


    # Enter a parse tree produced by JarvisLangParser#printStmt.
    def enterPrintStmt(self, ctx:JarvisLangParser.PrintStmtContext):
        pass

    # Exit a parse tree produced by JarvisLangParser#printStmt.
    def exitPrintStmt(self, ctx:JarvisLangParser.PrintStmtContext):
        pass


    # Enter a parse tree produced by JarvisLangParser#readStmt.
    def enterReadStmt(self, ctx:JarvisLangParser.ReadStmtContext):
        pass

    # Exit a parse tree produced by JarvisLangParser#readStmt.
    def exitReadStmt(self, ctx:JarvisLangParser.ReadStmtContext):
        pass


    # Enter a parse tree produced by JarvisLangParser#addStmt.
    def enterAddStmt(self, ctx:JarvisLangParser.AddStmtContext):
        pass

    # Exit a parse tree produced by JarvisLangParser#addStmt.
    def exitAddStmt(self, ctx:JarvisLangParser.AddStmtContext):
        pass


    # Enter a parse tree produced by JarvisLangParser#subStmt.
    def enterSubStmt(self, ctx:JarvisLangParser.SubStmtContext):
        pass

    # Exit a parse tree produced by JarvisLangParser#subStmt.
    def exitSubStmt(self, ctx:JarvisLangParser.SubStmtContext):
        pass


    # Enter a parse tree produced by JarvisLangParser#mulStmt.
    def enterMulStmt(self, ctx:JarvisLangParser.MulStmtContext):
        pass

    # Exit a parse tree produced by JarvisLangParser#mulStmt.
    def exitMulStmt(self, ctx:JarvisLangParser.MulStmtContext):
        pass


    # Enter a parse tree produced by JarvisLangParser#divStmt.
    def enterDivStmt(self, ctx:JarvisLangParser.DivStmtContext):
        pass

    # Exit a parse tree produced by JarvisLangParser#divStmt.
    def exitDivStmt(self, ctx:JarvisLangParser.DivStmtContext):
        pass


    # Enter a parse tree produced by JarvisLangParser#incrementStmt.
    def enterIncrementStmt(self, ctx:JarvisLangParser.IncrementStmtContext):
        pass

    # Exit a parse tree produced by JarvisLangParser#incrementStmt.
    def exitIncrementStmt(self, ctx:JarvisLangParser.IncrementStmtContext):
        pass


    # Enter a parse tree produced by JarvisLangParser#decrementStmt.
    def enterDecrementStmt(self, ctx:JarvisLangParser.DecrementStmtContext):
        pass

    # Exit a parse tree produced by JarvisLangParser#decrementStmt.
    def exitDecrementStmt(self, ctx:JarvisLangParser.DecrementStmtContext):
        pass


    # Enter a parse tree produced by JarvisLangParser#ifStmt.
    def enterIfStmt(self, ctx:JarvisLangParser.IfStmtContext):
        pass

    # Exit a parse tree produced by JarvisLangParser#ifStmt.
    def exitIfStmt(self, ctx:JarvisLangParser.IfStmtContext):
        pass


    # Enter a parse tree produced by JarvisLangParser#elseStmt.
    def enterElseStmt(self, ctx:JarvisLangParser.ElseStmtContext):
        pass

    # Exit a parse tree produced by JarvisLangParser#elseStmt.
    def exitElseStmt(self, ctx:JarvisLangParser.ElseStmtContext):
        pass


    # Enter a parse tree produced by JarvisLangParser#repeatStmt.
    def enterRepeatStmt(self, ctx:JarvisLangParser.RepeatStmtContext):
        pass

    # Exit a parse tree produced by JarvisLangParser#repeatStmt.
    def exitRepeatStmt(self, ctx:JarvisLangParser.RepeatStmtContext):
        pass


    # Enter a parse tree produced by JarvisLangParser#typeSpec.
    def enterTypeSpec(self, ctx:JarvisLangParser.TypeSpecContext):
        pass

    # Exit a parse tree produced by JarvisLangParser#typeSpec.
    def exitTypeSpec(self, ctx:JarvisLangParser.TypeSpecContext):
        pass


    # Enter a parse tree produced by JarvisLangParser#comparison.
    def enterComparison(self, ctx:JarvisLangParser.ComparisonContext):
        pass

    # Exit a parse tree produced by JarvisLangParser#comparison.
    def exitComparison(self, ctx:JarvisLangParser.ComparisonContext):
        pass


    # Enter a parse tree produced by JarvisLangParser#expression.
    def enterExpression(self, ctx:JarvisLangParser.ExpressionContext):
        pass

    # Exit a parse tree produced by JarvisLangParser#expression.
    def exitExpression(self, ctx:JarvisLangParser.ExpressionContext):
        pass


    # Enter a parse tree produced by JarvisLangParser#additiveExpr.
    def enterAdditiveExpr(self, ctx:JarvisLangParser.AdditiveExprContext):
        pass

    # Exit a parse tree produced by JarvisLangParser#additiveExpr.
    def exitAdditiveExpr(self, ctx:JarvisLangParser.AdditiveExprContext):
        pass


    # Enter a parse tree produced by JarvisLangParser#multiplicativeExpr.
    def enterMultiplicativeExpr(self, ctx:JarvisLangParser.MultiplicativeExprContext):
        pass

    # Exit a parse tree produced by JarvisLangParser#multiplicativeExpr.
    def exitMultiplicativeExpr(self, ctx:JarvisLangParser.MultiplicativeExprContext):
        pass


    # Enter a parse tree produced by JarvisLangParser#factor.
    def enterFactor(self, ctx:JarvisLangParser.FactorContext):
        pass

    # Exit a parse tree produced by JarvisLangParser#factor.
    def exitFactor(self, ctx:JarvisLangParser.FactorContext):
        pass



del JarvisLangParser