#include <clang-c/index.h>

enum CXChildVisitResult foundChild(CXCursor cursor, CXCursor parent, CXClientData client_data)
{
    printf("%d", clang_getCursorLanguage(cursor));

    return CXChildVisit_Recurse;
}

int main()
{
    CXTranslationUnit tu;
    CXIndex idx;
    CXCursor cur;

    idx = clang_createIndex(1, 0);
    tu = clang_createTranslationUnitFromSourceFile(idx, "test.c", 0, NULL, 0, NULL);
    cur = clang_getTranslationUnitCursor(tu);

    clang_visitChildren(cur, foundChild, NULL);
}
