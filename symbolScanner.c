#include <clang-c/index.h>

enum CXChildVisitResult foundChild(CXCursor cursor, CXCursor parent, CXClientData client_data)
{
    if(clang_getCursorKind(cursor) == CXCursor_CallExpr)
    {
        printf("%s\n", clang_getCString(clang_getCursorSpelling(cursor)));
    }

    return CXChildVisit_Recurse;
}

int main()
{
    CXTranslationUnit tu;
    CXIndex idx;
    CXCursor cur;

    idx = clang_createIndex(1, 0);
    tu = clang_createTranslationUnitFromSourceFile(idx, "symbolScanner.c", 0, NULL, 0, NULL);
    cur = clang_getTranslationUnitCursor(tu);

    clang_visitChildren(cur, foundChild, NULL);
}
