#include <clang-c/index.h>
#include <stdio.h>
#include <stdlib.h>

enum CXChildVisitResult foundChild(CXCursor cursor, CXCursor parent, CXClientData client_data)
{
    if(clang_getCursorKind(cursor) == CXCursor_CallExpr)
    {
        printf("%s\n", clang_getCString(clang_getCursorSpelling(cursor)));
    }

    return CXChildVisit_Recurse;
}

int main(int argc, char ** argv)
{
    CXTranslationUnit tu;
    CXIndex idx;
    CXCursor cur;
    char * filename;

    if(argc != 2)
    {
        printf("Usage: %s source_filename.c\n", argv[0]);
        return EXIT_FAILURE;
    }

    filename = argv[1];
    idx = clang_createIndex(1, 0);
    tu = clang_createTranslationUnitFromSourceFile(idx, filename, 0, NULL, 0, NULL);
    cur = clang_getTranslationUnitCursor(tu);

    clang_visitChildren(cur, foundChild, NULL);

    return EXIT_SUCCESS;
}
