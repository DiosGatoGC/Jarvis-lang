# Generated from JarvisLang.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .JarvisLangParser import JarvisLangParser
else:
    from JarvisLangParser import JarvisLangParser

# This class defines a complete generic visitor for a parse tree produced by JarvisLangParser.

class JarvisLangVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by JarvisLangParser#program.
    def visitProgram(self, ctx:JarvisLangParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JarvisLangParser#statement.
    def visitStatement(self, ctx:JarvisLangParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JarvisLangParser#varDecl.
    def visitVarDecl(self, ctx:JarvisLangParser.VarDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JarvisLangParser#constDecl.
    def visitConstDecl(self, ctx:JarvisLangParser.ConstDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JarvisLangParser#assignment.
    def visitAssignment(self, ctx:JarvisLangParser.AssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JarvisLangParser#printStmt.
    def visitPrintStmt(self, ctx:JarvisLangParser.PrintStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JarvisLangParser#readStmt.
    def visitReadStmt(self, ctx:JarvisLangParser.ReadStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JarvisLangParser#addStmt.
    def visitAddStmt(self, ctx:JarvisLangParser.AddStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JarvisLangParser#subStmt.
    def visitSubStmt(self, ctx:JarvisLangParser.SubStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JarvisLangParser#mulStmt.
    def visitMulStmt(self, ctx:JarvisLangParser.MulStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JarvisLangParser#divStmt.
    def visitDivStmt(self, ctx:JarvisLangParser.DivStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JarvisLangParser#incrementStmt.
    def visitIncrementStmt(self, ctx:JarvisLangParser.IncrementStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JarvisLangParser#decrementStmt.
    def visitDecrementStmt(self, ctx:JarvisLangParser.DecrementStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JarvisLangParser#ifStmt.
    def visitIfStmt(self, ctx:JarvisLangParser.IfStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JarvisLangParser#elseStmt.
    def visitElseStmt(self, ctx:JarvisLangParser.ElseStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JarvisLangParser#repeatStmt.
    def visitRepeatStmt(self, ctx:JarvisLangParser.RepeatStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JarvisLangParser#typeSpec.
    def visitTypeSpec(self, ctx:JarvisLangParser.TypeSpecContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JarvisLangParser#comparison.
    def visitComparison(self, ctx:JarvisLangParser.ComparisonContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JarvisLangParser#expression.
    def visitExpression(self, ctx:JarvisLangParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JarvisLangParser#additiveExpr.
    def visitAdditiveExpr(self, ctx:JarvisLangParser.AdditiveExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JarvisLangParser#multiplicativeExpr.
    def visitMultiplicativeExpr(self, ctx:JarvisLangParser.MultiplicativeExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JarvisLangParser#factor.
    def visitFactor(self, ctx:JarvisLangParser.FactorContext):
        return self.visitChildren(ctx)



del JarvisLangParser